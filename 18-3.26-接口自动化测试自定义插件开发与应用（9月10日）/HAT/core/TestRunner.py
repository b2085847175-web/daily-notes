# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : TestRunner.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import copy
import sys

import allure
import pytest
import requests
from tqdm import tqdm

from HAT.context.ApiCaseContext import ApiCaseContext
from HAT.core.globalContext import g_context
from HAT.extend.script import run_script
from HAT.keywords.api_keywords import Keywords
from HAT.parse.ExcelCaseParser import load_excel_files, excel_case_parser
from HAT.parse.YamlCaseParser import readYaml, load_context_from_yaml, load_yaml_files, yaml_case_parser
from HAT.utils.VarRender import refresh
from HAT.utils.allure_step_logger import allure_step_with_log


#拿到数据，调度执行yaml用例

class TestRunner:

    # data=readYaml(r'./examples/api-cases-yaml/1_login.yaml')  #拿到yaml用例数据
    # data=load_yaml_files(r'./examples/api-cases-yaml/')
    # alldata=yaml_case_parser(r'./examples/api-cases-yaml/')#返回字典
    # data=alldata["case_infos"]

    # alldata=yaml_case_parser(r'./examples/api-cases-商城/')
    # data=alldata["case_infos"]
    # print("yaml用例数据",data)
    # @pytest.mark.parametrize('caseinfo',data)  #一定是一个列表数据  会把列表去掉
    def test_case_exceute(self,caseinfo):
        # 固定传requests或者requests.session()
        # keywords=Keywords(requests)
        # 基础配置是测试报告用的
        base_info=caseinfo.get('基础配置',{})

        if base_info.get("用例类型")=='ApiCase':
            keywords=ApiCaseContext().init_keywords()
        allure.dynamic.parameter("caseinfo","")
        allure.dynamic.feature(base_info.get("一级模块","默认模块"))
        allure.dynamic.story(base_info.get("二级模块","默认模块"))
        allure.dynamic.title(base_info.get("用例标题","默认用例标题"))
        #注意：在测试报告中看功能这个地方

        local_context=caseinfo.get("local_context",{})#后期外部数据可以放在local_context变量名中，现在没有用到。讲ddt时会用到
        context=copy.deepcopy(g_context().show_dict())#复制全局变量
        context.update(local_context)

        pre_script=refresh(caseinfo.get("前置脚本",None),context)#获取前置脚本的数据
        print("前置脚本数据",pre_script) #["context.update({'name':'youer'})"]
        print("没有更新全局变量", g_context().show_dict())
        if pre_script:
            for script in eval(pre_script):
                #把前置脚本的数据放在全局变量
                run_script.exec_script(script,g_context().show_dict())#全局变量有个有个url
                print("更新全局变量",g_context().show_dict())


        # 用例步骤具体要执行的接口  不是所有的数据，需要处理一下，拿到我想要的数据
        steps = caseinfo.get('用例步骤', None) #[{发送登陆接口:{操作类型: 发送请求POST,xxxx}}]
        with tqdm(total=len(steps),desc="开始执行")as pbar:
            for step in steps:
                step_name=list(step.keys())[0]  #发送登陆接口
                step_value=list(step.values())[0]  #url:"{{url}}"
                print("没有渲染之前的用例数据",step_value)
                # print("接口具体数据",step_value)
                pbar.set_description(f'{base_info.get("用例标题")}-当前步骤:{step_name}')
                pbar.update(1)#进度格
                with allure_step_with_log(step_name):
                # with allure.step(step_name):
                    key=step_value['操作类型']#发送请求POST 发送请求get
                    # print("拿到请求类型",key)
                    context=copy.deepcopy(g_context().show_dict())#拿全局变量的值 深拷贝 不影响到原来的数据
                    context.update(local_context)#把ddt的数据放在全局变量
                    step_value=eval(refresh(step_value,context)) #url:"http://shop-xo"
                    print("渲染之后的用例数据", step_value)
                    try:
                        key_func=keywords.__getattribute__(key)  #在Keywords类中找 发送请求POST  key_func=发送请求POST
                        key_func(**step_value)  # key_func是什么值  发送请求POST()  调用函数
                    except AttributeError:  #优化一下  没有找到方法去另外的目录里面找一下(key_dir)
                        if g_context().get_dict("key_dir") is not None:
                            keywords.ex_invoke(key=key,step_value=step_value)
                        # sys.path.append('./HAT/key_dir')#找目录文件
                        # module=__import__(key)#导入模块
                        # class_=getattr(module,key)#获取模块中的方法
                        # key_func=class_(requests).__getattribute__(key)
                    except Exception as e: #也没有找到就抛出异常
                        raise e



        local_context = caseinfo.get("local_context", {})  # 后期外部数据可以放在local_context变量名中，现在没有用到。讲ddt时会用到
        context = copy.deepcopy(g_context().show_dict())  # 复制全局变量
        context.update(local_context)

        pre_script = refresh(caseinfo.get("后置脚本", None), context)  # 获取前置脚本的数据
        print("后置脚本", pre_script)  # ["context.update({'name':'youer'})"]
        if pre_script:
            for script in eval(pre_script):
                # 把前置脚本的数据放在全局变量
                run_script.exec_script(script, g_context().show_dict())  # 全局变量有个有个url


#能运行1  不能运行2




