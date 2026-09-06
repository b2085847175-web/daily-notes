# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : 发送请求POST.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import allure


class 发送请求POST:
# 参数不能写死  python **kwargs 接受很多关键字参数

    def __init__(self,request):
        self.request=request

    @allure.step("发送请求POST")
    def 发送请求POST(self, **kwargs):
        url = kwargs.get("请求地址",
                         None)  # 没获取到地址给个None  http://shop-xo.hctestedu.com/index.php?s=/api/user/login&application=app&application_client_type=weixin
        data = kwargs.get("请求数据", None)  # {"accounts": "youtian", "pwd": "123456","type": "username"}
        params = kwargs.get("URL参数", None)
        headers = kwargs.get("请求头", None)
        files = kwargs.get("文件列表", [])
        data_type = kwargs.get("请求类型", "data").lower()  # 默认请求数据类型  取决于content-type

        # 构造统一的请求参数字典  requests.post(**requests_data)
        requests_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "files": files,
        }

        # 区分传参类型（json传参还是 data传参）
        if data_type == 'json':
            requests_data["json"] = data
        elif data_type == "data":
            requests_data["data"] = data
        else:
            raise Exception("请求类型错误，仅支持json/data")

        # 发送请求+异常处理  requests.request("post",**requests_data)==requests.post(url,params=params,json=xxx)
        try:
            response = self.request.request("post", **requests_data)
            print("发送结果", response.json())
            return response
        except Exception as e:
            print("post发送请求失败")
            raise
