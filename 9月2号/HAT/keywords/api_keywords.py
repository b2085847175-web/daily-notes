# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : requests二次封装.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import allure
import jsonpath
import requests
from deepdiff import DeepDiff

from HAT.core.globalContext import g_context


#封装的好处：每次要用的时候，直接调用这个函数，更改的时候只要更改这个函数即可
# 一处修改，处处生效
class Keywords:
    # request传requests /requests.session
    def __init__(self,request):
        self.request=request

    #参数不能写死  python **kwargs 接受很多关键字参数
    @allure.step("发送请求POST")
    def 发送请求POST(self,**kwargs):
        url=kwargs.get("请求地址",None)#没获取到地址给个None  http://shop-xo.hctestedu.com/index.php?s=/api/user/login&application=app&application_client_type=weixin
        data=kwargs.get("请求数据",None) #{"accounts": "youtian", "pwd": "123456","type": "username"}
        params=kwargs.get("URL参数",None)
        headers=kwargs.get("请求头",None)
        files=kwargs.get("文件列表",[])
        data_type=kwargs.get("请求类型","data").lower()#默认请求数据类型  取决于content-type

        # 构造统一的请求参数字典  requests.post(**requests_data)
        requests_data={
            "url":url,
            "params":params,
            "headers":headers,
            "files":files,
        }

        #区分传参类型（json传参还是 data传参）
        if data_type=='json':
            requests_data["json"]=data
        elif data_type=="data":
            requests_data["data"] = data
        else:
            raise Exception("请求类型错误，仅支持json/data")

        #发送请求+异常处理  requests.request("post",**requests_data)==requests.post(url,params=params,json=xxx)
        try:
            response=self.request.request("post",**requests_data)
            print("发送结果",response.json())

            g_context().set_dict("响应结果",response) #把返回结果放在全局变量
            return response
        except Exception as e:
            print("post发送请求失败")
            raise

    @allure.step("发送请求GET")
    def 发送请求GET(self,**kwargs):
        url = kwargs.get('请求地址', None)
        params = kwargs.get('URL参数', None)
        headers = kwargs.get('请求头', None)
        data = kwargs.get('请求数据', None)
        files = kwargs.get('文件列表', [])
        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "files": files,
        }
        response = self.request.request("get", **request_data)
        return response

    @allure.step("提取数据JSON")
    def 提取数据JSON(self,**kwargs):
        EXPRESSION=kwargs.get("表达式",None) #$.token

        INDEX=kwargs.get("下标",None)#取到很多值的时候，你自己给个你想要提取哪个值的下标  默认取第一值
        if INDEX is None:
            INDEX=0

        response=g_context().get_dict("响应结果").json()
        result=jsonpath.jsonpath(response, EXPRESSION)
        if not result:
            raise Exception(f"没有找到对应的数据:{EXPRESSION}")
        ex_data=result[INDEX]  #具体取到你要的数据

        g_context().set_dict(kwargs["变量名"],ex_data)
        print("全局变量中有没token值",g_context().show_dict())

    @allure.step("断言文本")
    def 断言文本(self,**kwargs):
        #比较器  == !=
        comparators={
            "==":lambda a,b:a==b,
            ">=":lambda a,b:a>=b,
            "<=": lambda a, b: a <= b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            "in": lambda a, b: a in b,
        }

        message=kwargs.get("错误信息",None)#用例有没有传错误信息
        operators=kwargs.get("比较符",'==')#用例有没有传比较符  没有传默认==
        compare_type=kwargs.get("断言类型","文本")#用例有没有传断言类型，没有就默认文本

        #判断你传过来的比较符在不在比较器里面，不在就报错
        if operators not in comparators:
            raise Exception(f"没有对应的比较符{operators}")

        #如果你传过来的是数字，把期望结果转成数字
        if compare_type=="数字":
            kwargs["期望结果"]=float(kwargs["期望结果"])
        else:
            kwargs["期望结果"] = str(kwargs["期望结果"])

        #预期结果和实际结果的对比
        #if not  True ==false      登陆成功 == 登陆成功    if false 不进入判断  没有任何提示  断言成功
        # if not  False== True == 登陆成功 用户名或密码错误  if true 进入判断：
        # 2<  1
        if not comparators[operators](kwargs["实际结果"],kwargs["期望结果"]):
            if message: #登陆错误
                raise Exception(message)
            else: #登陆成功==用户名或密码错误 失败
                raise Exception(f"{kwargs['实际结果']} {operators} {kwargs['期望结果']}失败")

    def 断言文本相等(self,**kwargs):
        kwargs.update({"比较符":"=="})
        self.断言文本(**kwargs)

    def 断言文本不相等(self,**kwargs):
        kwargs.update({"比较符":"!="})
        self.断言文本(**kwargs)

    def 断言文本包含(self, **kwargs):
        kwargs.update({"比较符": "in"})
        self.断言文本(**kwargs)

    def 断言数字相等(self, **kwargs):
        kwargs.update({"比较符": "==","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字大于等于(self, **kwargs):
        kwargs.update({"比较符": ">=","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字小于等于(self, **kwargs):
        kwargs.update({"比较符": "<=","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字不等于(self, **kwargs):
        kwargs.update({"比较符": "!=","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字小于(self, **kwargs):
        kwargs.update({"比较符": "<","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字大于(self, **kwargs):
        kwargs.update({"比较符": ">","断言类型":"数字"})
        self.断言文本(**kwargs)


    def 批量断言(self,**kwargs):
        try:
            exmsg=kwargs["期望结果"]
            #从全局变量拿到实际结果
            sjmsg=g_context().get_dict("响应结果").json()
            exclude_paths=kwargs.get("过滤字段",[])
            ignore_string_case=kwargs.get("忽略大小写",True)#没传值就是默认忽略大小写
            ignore_order=kwargs.get("忽略顺序",True)#没传值就是默认忽略顺序

            screen_data={
                "exclude_paths":exclude_paths,
                "ignore_string_case":ignore_string_case,
                "ignore_order":ignore_order
            }
            diff=DeepDiff(sjmsg,exmsg,**screen_data)
        except Exception as e:
            assert False,f"批量断言失败,{e}"
        assert not diff,f"批量断言失败{diff.pretty()}"

