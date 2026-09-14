import copy
import sys

import allure
import pytest
import requests
from tqdm import tqdm

from HAT.core.globalContext import g_context
from HAT.extend.script import run_script
from HAT.keywords.api_keywords import Keywords
from HAT.parse.YamlCaseParser import load_context_from_yaml, readYaml
from HAT.utils.VarRender import refresh


class TestRunner:
    load_context_from_yaml(r'./examples/api-cases-yaml/')
    data = readYaml(r'./examples/api-cases-yaml/login.yaml')

    @pytest.mark.parametrize('caseinfo', data)
    def test_case_exceute(self, caseinfo):
        keywords = Keywords(requests)
        base_info = caseinfo.get('基础配置', {})

        allure.dynamic.parameter('caseinfo', '')
        allure.dynamic.feature(base_info.get('一级模块', '默认模块'))
        allure.dynamic.story(base_info.get('二级模块', '默认模块'))
        allure.dynamic.title(base_info.get('用例标题', '默认用例标题'))

        local_context = caseinfo.get('local_context', {})
        context = copy.deepcopy(g_context().show_dict())
        context.update(local_context)

        pre_script = refresh(caseinfo.get('前置脚本', None), context)
        print('前置脚本数据', pre_script)
        print('没有更新全局变量', g_context().show_dict())
        if pre_script:
            for script in eval(pre_script):
                run_script.exec_script(script, g_context().show_dict())
                print('更新全局变量', g_context().show_dict())

        steps = caseinfo.get('用例步骤', None)
        with tqdm(total=len(steps), desc='开始执行') as pbar:
            for step in steps:
                step_name = list(step.keys())[0]
                step_value = list(step.values())[0]
                print('没有渲染之前的用例数据', step_value)
                pbar.set_description(f'{base_info.get("用例标题")}-当前步骤:{step_name}')
                pbar.update(1)

                with allure.step(step_name):
                    key = step_value['操作类型']
                    context = copy.deepcopy(g_context().show_dict())
                    step_value = eval(refresh(step_value, context))
                    print('渲染之后的用例数据', step_value)

                    try:
                        key_func = keywords.__getattribute__(key)
                    except AttributeError:
                        sys.path.append('./HAT/key_dir')
                        module = __import__(key)
                        class_ = getattr(module, key)
                        key_func = class_(requests).__getattribute__(key)
                    except Exception as e:
                        raise e

                    key_func(**step_value)

        local_context = caseinfo.get('local_context', {})
        context = copy.deepcopy(g_context().show_dict())
        context.update(local_context)

        post_script = refresh(caseinfo.get('后置脚本', None), context)
        print('后置脚本', post_script)
        if post_script:
            for script in eval(post_script):
                run_script.exec_script(script, g_context().show_dict())
