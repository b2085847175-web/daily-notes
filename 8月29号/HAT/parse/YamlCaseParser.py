import json
from pathlib import Path

import yaml

from HAT.core.globalContext import g_context


PROJECT_DIR = Path(__file__).resolve().parents[2]


def readYaml(file_path):
    path = Path(file_path)
    if not path.is_absolute():
        path = PROJECT_DIR / path

    with path.open('r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    return [data] if not isinstance(data, list) else data


def load_context_from_yaml(folder_path):
    path = Path(folder_path)
    if not path.is_absolute():
        path = PROJECT_DIR / path

    yaml_file_path = path / 'context.yaml'
    with yaml_file_path.open('r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    if data:
        g_context().set_by_dict(data)

    print('全局变量', g_context().show_dict())
