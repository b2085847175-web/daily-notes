import allure


class 发送请求POST:
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

        response = self.request.request('post', **requests_data)
        print('发送结果', response.json())
        return response
