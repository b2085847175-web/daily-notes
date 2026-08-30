import json

from jinja2 import Template


def refresh(target, context):
    """把数据中的 {{变量名}} 替换成全局变量里的真实值"""
    if target is None:
        return None

    if isinstance(target, (dict, list)):
        target_str = json.dumps(target, ensure_ascii=False)
    else:
        target_str = str(target)

    return Template(target_str).render(context)
