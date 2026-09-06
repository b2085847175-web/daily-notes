# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : ApiCaseContext.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import requests

from HAT.core.globalContext import g_context
from HAT.keywords.api_keywords import Keywords


_global_request_obj=None
#专门处理session会话的
class ApiCaseContext:
    def __init__(self):
        self.request=None
        self.keywords=None

    #session复用和不复用怎么处理
    def init_keywords(self):
        #session复用 context.yaml
        session_reuse=g_context().get_dict("session_reuse")
        # 如果session_reuse是True 创建一个session对象，保存在全局变量中，后续用例复用同一个session对象
        if session_reuse is not None and session_reuse==True:
            global _global_request_obj  #模块级的全局变量
            if _global_request_obj is None: #如果全局变量没有值，新建一个session对象
                _global_request_obj=requests.session()
            self.request=_global_request_obj
        else: #False 每次都创建session对象  每次用的都是最新的
            self.request=requests.session()
        self.keywords=Keywords(self.request)
        return self.keywords

#封装了没有调用方法