# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : VarRender.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import json

from jinja2 import Template


def refresh(target,context):
    """
    变量渲染：把数据中的 {{变量名}} 替换成实际的值
    :param target: 目标字符串，字符串数据，有一个字符串模板 '{{变量名}}'   '{{URL}}'
    :param context: 源字典  字典数据{'键':'值','键':'值'}     {'URL': 'http://shop-xo.hctestedu.com'}
    :return:
    安装一个库  jinja2
    """
    #如果传过来的数据是None,直接返回None
    if target is None:
        return None

    #如果target是字典或列表，转成字符串
    #否则，直接用str转成字符串
    if isinstance(target,(dict,list)):
        target_str=json.dumps(target,ensure_ascii=False)
    else:
        target_str=str(target)

    return Template(target_str).render(context)
# target_str 必须是字符串
# 把字符串变成一个模板对象，用context字典中的值，替换成模板中的{{变量名}}

if __name__ == '__main__':
    context = {'URL': 'http://shop-xo.hctestedu.com',"age":"18","name":"李四"}
    target = '{"name":"张三","age":"{{age}}"}'
    r = refresh(target, context)
    print("新数据", r)


    # context={'URL': 'http://shop-xo.hctestedu.com'}
    # target='{{URL}}'
    # r=refresh(target,context)
    # print("新数据",r)

