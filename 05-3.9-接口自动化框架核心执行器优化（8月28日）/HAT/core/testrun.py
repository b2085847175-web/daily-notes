import sys
from pathlib import Path

import allure
import pytest
from tqdm import tqdm

import requests

from HAT.keywords.api_client import Keywords
from HAT.parse.读取文件 import readyaml


client = Keywords(requests.session())
KEY_DIR = Path(__file__).resolve().parents[1] / 'key_dir'


class TestRun:
    # 只执行包含用例步骤的 YAML，跳过 test.yaml 这类语法学习文件
    data = [
        case
        for case in readyaml('./examples/api-cases-yaml')
        if case.get('用例步骤')
    ]

    @pytest.mark.parametrize('data_yaml', data)
    def test_case_yaml(self, data_yaml):
        base_info = data_yaml.get('基础配置', {})
        allure.dynamic.parameter('caseinfo', '')
        allure.dynamic.feature(base_info.get('一级模块', '默认模块'))
        allure.dynamic.story(base_info.get('二级模块', '默认模块'))
        allure.dynamic.title(base_info.get('用例标题', '默认用例标题'))

        steps = data_yaml.get('用例步骤', [])
        assert steps, '用例缺少用例步骤'

        with tqdm(total=len(steps), desc='开始执行') as pbar:
            for step in steps:
                step_name, step_value = next(iter(step.items()))
                key = step_value.get('操作类型')
                pbar.set_description(f'{base_info.get("用例标题", "默认用例标题")}-当前步骤:{step_name}')
                pbar.update(1)

                with allure.step(step_name):
                    try:
                        key_func = client.__getattribute__(key)
                    except AttributeError:
                        if str(KEY_DIR) not in sys.path:
                            sys.path.append(str(KEY_DIR))

                        try:
                            module = __import__(key)
                            class_ = getattr(module, key)
                            key_func = class_(requests).__getattribute__(key)
                        except (ImportError, AttributeError) as e:
                            raise AssertionError(f'{step_name} 没有找到关键字方法：{key}') from e
                    except Exception as e:
                        raise e

                    response = key_func(**step_value)
                    print(step_name, response.status_code, response.json())
