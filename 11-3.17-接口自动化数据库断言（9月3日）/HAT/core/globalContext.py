# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : globalContext.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈

#全局变量的类
class g_context:
    _dic={} #设置的是一个类变量  实现共享数据

    # 设置字典  g_context().set_dict('name','Alice')  _dic={"name":"Alice"}
    def set_dict(self,key,value):
        self._dic[key]=value

    #设置字典 完整的字典 g_context().set_by_dict({"age":"18"})  _dic={"name":"Alice","age":"18"}
    def set_by_dict(self,dic):
        self._dic.update(dic)

    #得到字典值 g_context().get_dict("age") 18
    def get_dict(self,key):
        return self._dic.get(key,None)

    #得到到字典   _dic={"name":"Alice","age":"18"}
    def show_dict(self):
        return self._dic