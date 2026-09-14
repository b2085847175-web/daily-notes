# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : YamlCaseParser.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import copy
import os.path
import uuid

import yaml

from HAT.core.globalContext import g_context


#专门读取yaml文件数据

#打开文件，读取数据内容
def readYaml(file_path):
    case_info=[]
    with open(file_path,'r',encoding='utf-8') as f:
        data=yaml.load(f,Loader=yaml.FullLoader)#安全读取文件数据
        # print('yaml文件数据',data)
        case_info.append(data)
    return case_info

#把context.yaml数据读取出来
def load_context_from_yaml(file_path):
    """
    :param file_path: 文件夹
    :return:
    """
    yaml_file_path=os.path.join(file_path,'context.yaml')
    with open(yaml_file_path,'r',encoding="utf-8")as file:#打开文件
        data=yaml.load(file,Loader=yaml.FullLoader)#安全读取数据
        # print(data)
        if data:g_context().set_by_dict(data)
        # print("全局变量",g_context().show_dict())

#读取文件夹下符合规则的yaml文件
def load_yaml_files(file_path):
    """
    :param file_path: 文件夹
    :return:
    """
    #扫描整个文件夹
    yaml_caseInfos = []
    suite_folder=os.path.join(file_path)
    load_context_from_yaml(file_path)

    #规则 数字开头_分割.yaml，读取到了数据[(1,1_login.yaml)]
    file_names=[(int(f.split("_")[0]), f) for f in os.listdir(suite_folder)
     if f.endswith(".yaml") and f.split("_")[0].isdigit()]
    # print("符合规则的文件数据读取出来",file_names)
    file_names.sort()#排序
    file_names=[f[-1] for f in file_names]#文件名
    # print("排序后的文件名",file_names)

    #拿里面具体的数据
    for file_name in file_names:
        file_path=os.path.join(suite_folder,file_name)
        # print("文件具体位置",file_path)
        with open(file_path,'r',encoding='utf-8')as file:
            caseinfo=yaml.full_load(file)
            yaml_caseInfos.append(caseinfo)
    return yaml_caseInfos



# 代码思路：
# 1.用例结构拿出来
# 2.数据驱动的数据拿出来
# 3.组合：有几组数据驱动的数据组合成几条用例  组合第一条
#
# 正确用户名和密码+用例模板结合 1条用例
# 错误用户名和正确密码+用例模板  2条用例
# 正常用户名和错误密码+用例模板  3条用例

#解析ddt数据驱动  有几组ddt数据驱动就分解成几条用例
def yaml_case_parser(file_path):
    case_names=[]#存放所有标题
    case_infos=[]#存放所有用例
    #yaml用例数据都拿到
    yaml_caseInfos=load_yaml_files(file_path)

    for caseinfo in yaml_caseInfos:
        # print("yaml用例符合规则数据",caseinfo)
        ddts=caseinfo.get("数据驱动",[])  #数据驱动的数据拿出来
        # print("数据驱动拿出来",ddts)

        if len(ddts)==0:#没有数据驱动
            case_name = caseinfo.get("基础配置").get("用例标题", uuid.uuid4().__str__())
            case_names.append(case_name)#获取用例名称
            case_infos.append(caseinfo)#获取用例数据
        else: #有数据驱动
            caseinfo.pop("数据驱动")#用例结构拿出来
            for ddt in ddts:
                new_case=copy.deepcopy(caseinfo)#复制了一个新用例模板
                new_case.update({"local_context":ddt})#组合用例
                # print('组合的用例',new_case)
                # 获取用例标题，没有获取到用uuid生成
                case_name = caseinfo.get("基础配置").get("用例标题", uuid.uuid4().__str__())
                # 商城登录用例标题-正确用户名和密码   商城登录用例标题-错误用户名和正确密码    商城登录用例标题-正常用户名和错误密码
                case_name = f'{case_name}-{ddt.get("描述标题", uuid.uuid4().__str__())}'
                new_case.get("基础配置").update({"用例标题":case_name})
                # print('组合的用例', new_case)
                case_names.append(case_name)
                case_infos.append(new_case)
    return {
        "case_infos":case_infos,
        "case_names":case_names
    }





if __name__ == '__main__':
    # a=load_yaml_files(r'../../examples/api-cases-yaml/')
    # print("所有数据",a)

    a=yaml_case_parser(r'../../examples/api-cases-yaml/')
    print(a)

    # load_context_from_yaml(r'../../examples/api-cases-yaml/')

    # a=readYaml(r'../../examples/api-cases-yaml/1_login.yaml')
    # print(a)


# ./代表当前目录parse  ../代表是上一级目录HAT  ../../上上级目录day23  r 防止转义 /n /t