def exec_script(script, context):
    if script is None:
        return

    exec(script, {'context': context})
