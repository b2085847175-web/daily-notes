import pytest

import requests

from HAT.keywords.api_client import Keywords
from HAT.parse.YamlCaseParser import load_yaml_files


client = Keywords(requests.session())


class TestRun:
    # 只执行包含用例步骤的 YAML，跳过 test.yaml 这类语法学习文件
    data = [
        case
        for case in load_yaml_files('./examples/api-cases-yaml/')
        if case.get('用例步骤')
    ]

    @pytest.mark.parametrize('data_yaml', data)
    def test_case_yaml(self, data_yaml):
        steps = data_yaml.get('用例步骤', [])
        assert steps, '用例缺少用例步骤'

        for step in steps:
            step_name, step_value = next(iter(step.items()))
            key = step_value.get('操作类型')
            try:
                key_func = client.__getattribute__(key)
            except AttributeError:
                raise AssertionError(f'{step_name} 在 Keywords 中没有找到方法：{key}')

            response = key_func(**step_value)
            print(step_name, response.status_code, response.json())
