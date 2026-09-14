import os.path

import yaml

from HAT.core.globalContext import g_context


def readYaml(file_path):
    case_info = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        case_info.append(data)
    return case_info


def load_context_from_yaml(file_path):
    yaml_file_path = os.path.join(file_path, 'context.yaml')
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        if data:
            g_context().set_by_dict(data)
        print('全局变量', g_context().show_dict())
