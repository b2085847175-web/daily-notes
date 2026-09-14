# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : main.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import os
import sys
import time

import pytest
from allure_combine import combine_allure
from loguru import logger

from HAT.core.CasesPlugin import CasePlugin

#'-v','-s', 生成的数据比较详细
#--capture=sys系统配置  测试报告中会生成stdout附件
#--clean-alluredir 清空测试数据，保持测试报告中的数据是最新的测试数据
#--alluredir=allure-results
#alluredir生成测试数据    allure-results测试数据文件夹（可以更改名字）

#日志信息还可以放在文件中
#如果不存在logs就创建一个
if not os.path.exists('./HAT/logs'):
    os.mkdir('./HAT/logs')

#文件名称
time_str=time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
log_level=os.getenv("HAT_LOG_LEVEL","DEBUG").upper()#项目日志

#日志信息在控制台展示，在文件中展示
logger.configure(
    handlers=[
        {"sink":sys.stdout,"level":"INFO"},#控制台显示
        {"sink": os.path.join("./HAT/logs",f"hat_{time_str}.log"), "level": log_level}#文件中展示
    ]
)

# 执行用例并生成allure报告
pytest_ars=['-v','-s','--capture=sys',
            '--clean-alluredir',
            '--alluredir=allure-results',
            './HAT/core/TestRunner.py',
            '--type=yaml',
            '--cases=./examples/api-cases-商城'
            ]

# 执行用例  生成测试数据
pytest.main(pytest_ars,plugins=[CasePlugin()])

#生成测试报告  allure-report更改
os.system('allure generate -c -o allure-report')

combine_allure('./allure-report')#会生成一个complete.html可以在c/d盘打开
