import allure


class 发送请求POST:
    """动态关键字示例：文件名、类名、方法名都必须和操作类型一致"""

    def __init__(self, request):
        self.request = request

    @allure.step("发送请求POST")
    def 发送请求POST(self, **kwargs):
        request_data = {
            "url": kwargs.get("请求地址", None),
            "params": kwargs.get("URL参数", None),
            "headers": kwargs.get("请求头", None),
            "files": kwargs.get("文件列表", []),
        }

        data = kwargs.get("请求数据", None)
        data_type = kwargs.get("请求类型", "data").lower()

        if data_type == "json":
            request_data["json"] = data
        elif data_type == "data":
            request_data["data"] = data
        else:
            raise Exception("请求类型错误，仅支持json/data")

        response = self.request.request("post", **request_data)
        return response
