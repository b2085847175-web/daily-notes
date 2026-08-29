"""
requests 二次封装（教学版结构 + 英文命名）

结构参考 day08 的 Keywords 类：
- **kwargs 接收任意关键字参数，参数不写死
- kwargs.get(key, 默认值) 取值，取不到给默认值
- 按 data_type 自动区分 json / data 传参
- try/except 异常处理封装在内部，调用方不用重复写
"""

import requests


class ApiClient:
    """HTTP 请求客户端封装"""

    def __init__(self, session):
        # 传 requests 模块 -> 每次请求独立
        # 传 requests.session() -> 自动保持 cookie 会话
        self.session = session

    def send_post(self, **kwargs):
        url = kwargs.get("url", None)
        data = kwargs.get("data", None)
        params = kwargs.get("params", None)
        headers = kwargs.get("headers", None)
        files = kwargs.get("files", [])
        data_type = kwargs.get("data_type", "data").lower()

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
        except Exception as e:
            print("post发送请求失败")
            raise

    def send_get(self, **kwargs):
        url = kwargs.get("url", None)
        params = kwargs.get("params", None)
        headers = kwargs.get("headers", None)
        files = kwargs.get("files", [])
        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "files": files,
        }
        try:
            response = self.session.request("get", **request_data)
            return response
        except Exception as e:
            print("get发送请求失败")
            raise
