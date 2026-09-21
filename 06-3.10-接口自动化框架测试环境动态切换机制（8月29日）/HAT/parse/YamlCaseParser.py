# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : YamlCaseParser.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import os.path

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
        print("全局变量",g_context().show_dict())


if __name__ == '__main__':
    load_context_from_yaml(r'../../examples/api-cases-yaml/')

    a=readYaml(r'../../examples/api-cases-yaml/login.yaml')
    print(a)


# ./代表当前目录parse  ../代表是上一级目录HAT  ../../上上级目录day06  r 防止转义 /n /t
