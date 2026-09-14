import yaml

from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[2]


def readyaml(load):
    list_data = []

    path = Path(load)
    if not path.is_absolute():
        path = PROJECT_DIR / path

    if path.is_file():
        yaml_files = [path]
    else:
        yaml_files = sorted(path.glob('*.yaml')) + sorted(path.glob('*.yml'))

    if not yaml_files:
        raise FileNotFoundError(f'没有找到 YAML 文件：{path}')

    for yaml_file in yaml_files:
        with yaml_file.open('r', encoding='utf-8') as e:
            data = yaml.safe_load(e)

        if isinstance(data, list):
            list_data.extend(data)
        else:
            list_data.append(data)

    return list_data
