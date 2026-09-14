import json

from jinja2 import Template


def refresh(target, context):
    if target is None:
        return None

    if isinstance(target, (dict, list)):
        target_str = json.dumps(target, ensure_ascii=False)
    else:
        target_str = str(target)

    return Template(target_str).render(context)
