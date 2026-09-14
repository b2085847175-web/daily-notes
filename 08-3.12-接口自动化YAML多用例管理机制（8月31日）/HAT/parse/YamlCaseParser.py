import os

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


def load_yaml_files(file_path):
    yaml_case_infos = []
    suite_folder = os.path.join(file_path)
    load_context_from_yaml(file_path)

    file_names = [
        (int(f.split('_')[0]), f)
        for f in os.listdir(suite_folder)
        if f.endswith('.yaml') and f.split('_')[0].isdigit()
    ]
    file_names.sort()
    file_names = [f[-1] for f in file_names]

    for file_name in file_names:
        file_path = os.path.join(suite_folder, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            caseinfo = yaml.full_load(file)
            yaml_case_infos.append(caseinfo)

    return yaml_case_infos
