import json

import allure
import pytest
import requests

from HAT.keywords.api_client import Keywords
from HAT.core.globalContext import g_context
from HAT.parse.YamlCaseParser import load_context_from_yaml, readYaml
from HAT.utils.VarRender import refresh




load_context_from_yaml('examples/api-cases-yaml')
data = readYaml('examples/api-cases-yaml/login.yaml')


class TestRunner:
    @pytest.mark.parametrize('caseinfo', data)
    def test_case_exceute(self, caseinfo):
        keywords = Keywords(requests)
        base_info = caseinfo.get('基础配置', {})

        allure.dynamic.parameter('caseinfo', '')
        allure.dynamic.feature(base_info.get('一级模块', '默认模块'))
        allure.dynamic.story(base_info.get('二级模块', '默认模块'))
        allure.dynamic.title(base_info.get('用例标题', '默认用例标题'))

        steps = caseinfo.get('用例步骤', [])
        assert steps, '用例缺少用例步骤'

        for step in steps:
            step_name, step_value = next(iter(step.items()))
            print('没有渲染之前的用例数据', step_value)

            context = g_context().show_dict()
            rendered = refresh(step_value, context)
            step_value = json.loads(rendered)
            print('渲染之后的用例数据', step_value)

            key = step_value['操作类型']
            key_func = keywords.__getattribute__(key)
            response = key_func(**step_value)
            print('发送结果', response.status_code, response.json())
