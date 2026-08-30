import allure

import requests


class Keywords:
    def __init__(self, request):
        self.request = request

    @allure.step("发送请求POST")
    def 发送请求POST(self, **kwargs):
        url = kwargs.get("请求地址", None)
        data = kwargs.get("请求数据", None)
        params = kwargs.get("URL参数", None)
        headers = kwargs.get("请求头", None)
        files = kwargs.get("文件列表", [])
        data_type = kwargs.get("请求类型", "data").lower()

        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "files": files,
        }

        if data_type == "json":
            request_data["json"] = data
        elif data_type == "data":
            request_data["data"] = data
        else:
            raise Exception("请求类型错误，仅支持json/data")

        try:
            response = self.request.request("post", **request_data)
            return response
        except Exception:
            print("post发送请求失败")
            raise

    @allure.step("发送请求GET")
    def 发送请求GET(self, **kwargs):
        url = kwargs.get("请求地址", None)
        params = kwargs.get("URL参数", None)
        headers = kwargs.get("请求头", None)
        files = kwargs.get("文件列表", [])

        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "files": files,
        }

        try:
            response = self.request.request("get", **request_data)
            return response
        except Exception:
            print("get发送请求失败")
            raise
