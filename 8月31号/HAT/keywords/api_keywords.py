import allure
import jsonpath
import requests

from HAT.core.globalContext import g_context


class Keywords:
    def __init__(self, request):
        self.request = request

    @allure.step('发送请求POST')
    def 发送请求POST(self, **kwargs):
        url = kwargs.get('请求地址', None)
        data = kwargs.get('请求数据', None)
        params = kwargs.get('URL参数', None)
        headers = kwargs.get('请求头', None)
        files = kwargs.get('文件列表', [])
        data_type = kwargs.get('请求类型', 'data').lower()

        requests_data = {
            'url': url,
            'params': params,
            'headers': headers,
            'files': files,
        }

        if data_type == 'json':
            requests_data['json'] = data
        elif data_type == 'data':
            requests_data['data'] = data
        else:
            raise Exception('请求类型错误，仅支持json/data')

        try:
            response = self.request.request('post', **requests_data)
            print('发送结果', response.json())
            g_context().set_dict('响应结果', response)
            return response
        except Exception:
            print('post发送请求失败')
            raise

    @allure.step('发送请求GET')
    def 发送请求GET(self, **kwargs):
        url = kwargs.get('请求地址', None)
        params = kwargs.get('URL参数', None)
        headers = kwargs.get('请求头', None)
        files = kwargs.get('文件列表', [])

        request_data = {
            'url': url,
            'params': params,
            'headers': headers,
            'files': files,
        }

        response = self.request.request('get', **request_data)
        return response

    @allure.step('提取数据JSON')
    def 提取数据JSON(self, **kwargs):
        expression = kwargs.get('表达式', None)
        index = kwargs.get('下标', 0)
        if index is None:
            index = 0

        response = g_context().get_dict('响应结果').json()
        result = jsonpath.jsonpath(response, expression)
        if not result:
            raise Exception(f'没有找到对应的数据:{expression}')

        ex_data = result[index]
        g_context().set_dict(kwargs['变量名'], ex_data)
        print('全局变量中有没有token值', g_context().show_dict())
