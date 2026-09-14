# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : CasesPlugin.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
from HAT.core.globalContext import g_context
from HAT.parse.CaseParser import case_parser


class CasesPlugin:
    #pytest_addoption固定用法  添加自定义命令行选项
    def pytest_addoption(self,parser):
        parser.addoption("--type",action="store",help="测试用例类型")
        parser.addoption("--cases",action="store",help="测试用例目录")
        parser.addoption("--keyDir",action="store",help="扩展关键字目录")


    # pytest_generate_tests动态传参的方法,
    # metafunc固定用法  测试用例的元信息 里面有很多用例相关的信息
    def pytest_generate_tests(self,metafunc):
        case_type=metafunc.config.getoption("type")#yaml  excel
        case_dir=metafunc.config.getoption("cases")# ./examples/api-cases-商城
        key_dir=metafunc.config.getoption("keyDir")

        g_context().set_dict("key_dir", key_dir)

        # 调yaml方法 需要统一的调用方法 判断你传过来的是yaml调yaml方法传过来的是excel,调用excel
        data=case_parser(case_type,case_dir)

        #用例参数化  ids在控制台显示标题名称  data["case_infos"]用例数据传到caseinfo
        if "caseinfo" in metafunc.fixturenames:#检查用例里面有没有叫caseinfo的这个参数
            metafunc.parametrize("caseinfo",data["case_infos"], ids=data['case_names'])

    # 解决中文显示乱码问题
    def pytest_collection_modifyitems(self,items):
        for item in items:
            item.name=item.name.encode("utf-8").decode("unicode_escape")
            item._nodeid=item.nodeid.encode("utf-8").decode("unicode_escape")