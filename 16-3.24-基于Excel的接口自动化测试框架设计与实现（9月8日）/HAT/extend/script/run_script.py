# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : run_script.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈

def exec_script(script,context):
    """
    :param script: 前置脚本
    :param context: 全局变量
    :return:
    """
    if script is None:return
    exec(script,{"context":context})
    #b

#exec 是python内置函数 让字符串变成代码并执行 动态执行字符串的代码
#script 字符串脚本   context.update({'name':'youer'})
#context 全局变量 只有url地址，  context.update({'name':'youer'})  context={"url":"http://shop-xo.hctestedu.com"}
#执行后context变成{"url":"http://shop-xo.hctestedu.com",'name':'youer'}
