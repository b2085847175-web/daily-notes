# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : YamlCaseParser.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import os.path

import yaml


#专门读取yaml文件数据

#打开文件，读取数据内容
def readYaml(file_path):
    case_info=[]
    with open(file_path,'r',encoding='utf-8') as f:
        data=yaml.load(f,Loader=yaml.FullLoader)#安全读取文件数据
        # print('yaml文件数据',data)
        case_info.append(data)
    return case_info

#读取文件夹下符合规则的yaml文件
def load_yaml_files(file_path):
    """
    :param file_path: 文件夹
    :return:
    """
    #扫描整个文件夹
    yaml_caseInfos = []
    suite_folder=os.path.join(file_path)

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


if __name__ == '__main__':
    a=readYaml(r'../../examples/api-cases-yaml/1_login.yaml')
    print(a)

    # a=load_yaml_files(r'../../examples/api-cases-yaml/')
    # print("所有数据",a)


# ./代表当前目录parse  ../代表是上一级目录HAT  ../../上上级目录day05  r 防止转义 /n /t
