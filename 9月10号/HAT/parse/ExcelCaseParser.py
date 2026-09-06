# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : ExcelCaseParser.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import ast
import json
import os
import re
import uuid

import pandas as pd
import yaml

from HAT.core.globalContext import g_context


#专门处理数据库格式的函数
def load_dbinfo(name,all_sheets):
    """
    :param name: 名称
    :param all_sheets: 数据库数据
    :return:
    """
    db_config=all_sheets.fillna("").to_dict(orient="records")
    # print("数据库配置的数据",db_config)  #改造数据

    config_dict={}
    for item in db_config:
        db_info={}
        db_name=item.get("别名")  #mysql001  mysql002 dsw_mysql
        host=item.get("服务器IP")
        port=item.get("端口号")
        user=item.get("用户名")
        password=item.get("密码")
        db=item.get("数据库名称")
        # print("需要的数据",db_name,host,port,user,password,db)

        db_info.update({"host":host})
        db_info.update({"port":port})
        db_info.update({"user":user})
        db_info.update({"password":password})
        db_info.update({"db":db})
        # print(db_info)
        config_dict[db_name]=db_info
    # print(config_dict)
    return config_dict

#专门处理通用配置的数据
def load_configuration(name,all_sheets):
    config_dict={row["配置名"]:row["配置值"] for _,row in all_sheets.iterrows()}#循环所有的数据  iterrows() 是pandas DataFrame的方法，用于逐行遍历数据 _忽略这个索引
    # print("通用配置数据",config_dict)

    for key,value in config_dict.items():
        config_dict[key]=safe_convert_value(value)
    return config_dict

def load_context_from_excel(file_path):
    context_data={}
    #找到xlsx的数据位置在哪
    excel_file_path = os.path.join(file_path, 'context.xlsx')
    # print("读取excel路径",excel_file_path)

    # 读取数据 需要把xlsx的数据读取成和yaml一样的格式
    all_sheets=pd.read_excel(excel_file_path,sheet_name="数据库配置")
    config_dict=load_dbinfo("数据库配置",all_sheets)
    context_data.update({"_数据库":config_dict})
    # print("数据库配置的数据",context_data)


    all_sheets=pd.read_excel(excel_file_path, sheet_name="通用配置")
    config_dict = load_configuration("通用配置", all_sheets)
    context_data.update(config_dict)
    # print("通用配置",context_data)

    if context_data:g_context().set_by_dict(context_data)


#专门处理用例数据结构 一条用例多个步骤合并成yaml格式一样
def group_cases_by_title(data):
    current_case=None
    result=[]
    #循环用例里面有什么数据获取出来  获取你要的数据
    for row in data:
        title=row.get("用例标题")
        module_1=row.get("模块")
        module_2=row.get("功能")
        case_type=row.get("用例类型")
        step_desc=row.get("测试步骤")
        action_type=row.get("操作类型")
        data_content=row.get("数据内容")
        # print(title,module_1,module_2,case_type,step_desc,action_type,data_content)

        #处理数据内容
        data_content_dict={}#空字典
        if data_content is not None and data_content!="":
            pattern = r'(\w+)=(?:"([^"]*)"|(\S+))'#正则表达式 把key和值分开
            matches = re.findall(pattern, data_content)
            # print("匹配结果",matches)

            # [('请求地址', 'http://shop-xo.hctestedu.com', '')]  {请求地址: http://shop-xo.hctestedu.com}
            # key请求地址  quoted_value 带引号好的数据  unquoted_value不带引号的数据{"a":1}
            for key,quoted_value,unquoted_value in matches:
                value = quoted_value if quoted_value else unquoted_value #有引号的值先处理
                if value is not None:
                    data_content_dict[key]=safe_convert_value(value)  #安全的转化数据  /n /t {"accounts":"youyi"}
                else:
                    data_content_dict[key]=None
        # print("数据内容",data_content)

        if title is not None and title !="":#用例标题有数据
            if current_case is not None:  #把用例放到【】中
                result.append(current_case)
            current_case={"基础配置":{},"用例步骤":[]}
            current_case["基础配置"].update({"用例类型":case_type})
            current_case["基础配置"].update({"用例标题": title})
            current_case["基础配置"].update({"一级模块":module_1})
            current_case["基础配置"].update({"二级模块":module_2})
        if current_case is not None:
            current_case["用例步骤"].append({
                step_desc:{
                    "操作类型":action_type,
                    **data_content_dict
                }
            })
    if current_case is not None:  # 把所有的用例放到【】中
        result.append(current_case)
    return result

#安全数据类型转换  如果是字符串123  转成数字123  ”{a:1}“ {a:1}
def safe_convert_value(value_str):
    # 先检查输入类型，如果不是字符串就先转换成字符串
    if not isinstance(value_str, str):
        # 如果是数字、布尔值等非字符串类型，直接返回原值
        if isinstance(value_str, (int, float, bool)) or value_str is None:
            return value_str
        # 其他类型尝试转换成字符串处理
        value_str = str(value_str)

    # 使用 .strip() 方法去除字符串两端的空白字符
    value_str = value_str.strip()

    # 先尝试 JSON 解析（支持 true/false）
    try:
        return json.loads(value_str)
    except json.JSONDecodeError:
        pass

    # 再尝试 Python 字面量解析（支持单引号）
    try:
        return ast.literal_eval(value_str)
    except (SyntaxError, ValueError):
        return value_str

# yaml有什么要求，excel也有要求
# #读取文件夹下符合规则的excel文件
def load_excel_files(file_path):
    """
    :param file_path: 文件夹
    :return:
    """
    #扫描整个文件夹
    excel_caseInfos = []
    suite_folder=os.path.join(file_path)
    load_context_from_excel(file_path) #明天讲  读取context.xlsx数据

    #规则 数字开头_分割.xlsx，读取到了数据[(1,1_login.yaml)]
    file_names=[(int(f.split("_")[0]), f) for f in os.listdir(suite_folder)
     if f.endswith(".xlsx") and f.split("_")[0].isdigit()]
    # print("符合规则的文件数据读取出来",file_names)
    file_names.sort()#排序
    file_names=[f[-1] for f in file_names]#文件名
    # print("排序后的文件名",file_names)

    #拿里面具体的数据
    for file_name in file_names:
        file_path=os.path.join(suite_folder,file_name)
        #读取excel数据pandas读取excel
        data=pd.read_excel(file_path)
        # print("用例数据",data)
        data = data.where(data.notnull(), None) #None填充Nan
        # print("用例数据",data)
        data=data.to_dict(orient='records') #更加方便后面处理数据
        # print("用例数据", data)
        group_cases=group_cases_by_title(data)
        for case in group_cases:
            excel_caseInfos.append(case)
    return excel_caseInfos


#和yaml一样，统一数据格式case_ames用例标题名 cases_infos放用例
def excel_case_parser(config_path):
    case_names=[]
    cases_infos=[]
    excel_caseInfos=load_excel_files(config_path)#读取所有符合规则的xlsx用例数据
    for caseinfo in excel_caseInfos:#循环每条用例
        case_name=caseinfo.get("基础配置").get("用例标题",uuid.uuid4().__str__())#没有用例标题就生成一个
        case_names.append(case_name)
        cases_infos.append(caseinfo)
    return {
        "case_infos":cases_infos,
        "case_names":case_names
    }


if __name__ == '__main__':
    load_context_from_excel('../../examples/api-cases-excel')
    load_context=g_context().show_dict()
    with open("./context_excel数据.yaml",'w',encoding="utf-8") as file:
        yaml.dump(load_context,file,allow_unicode=True,sort_keys=False)
    # print("读取所有的excel用例数据",c)

    # c=load_excel_files('../../examples/api-cases-excel')
    # with open("./excel数据.yaml",'w',encoding="utf-8") as file:
    #     yaml.dump(c,file,allow_unicode=True,sort_keys=False)
    # # print("读取所有的excel用例数据",c)