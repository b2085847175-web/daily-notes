"""
requests 二次封装（教学版结构 + 英文命名）

结构参考 day08 的 Keywords 类：
- **kwargs 接收任意关键字参数，参数不写死
- kwargs.get(key, 默认值) 取值，取不到给默认值
- 按 data_type 自动区分 json / data 传参
- try/except 异常处理封装在内部，调用方不用重复写
"""

import allure

import requests


class Keywords:
    """requests 二次封装，方法名和 YAML 中的操作类型保持一致"""

    def __init__(self, session):
        # 传 requests 模块 -> 每次请求独立
        # 传 requests.session() -> 自动保持 cookie 会话
        self.session = session

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
            response = self.session.request("post", **request_data)
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
            response = self.session.request("get", **request_data)
            return response
        except Exception:
            print("get发送请求失败")
            raise


class ApiClient(Keywords):
    """兼容原来的英文命名"""

    def send_post(self, **kwargs):
        return self.发送请求POST(**kwargs)

    def send_get(self, **kwargs):
        return self.发送请求GET(**kwargs)
