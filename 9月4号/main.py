# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : main.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import os

import pytest
from allure_combine import combine_allure

#'-v','-s', 生成的数据比较详细
#--capture=sys系统配置  测试报告中会生成stdout附件
#--clean-alluredir 清空测试数据，保持测试报告中的数据是最新的测试数据
#--alluredir=allure-results
#alluredir生成测试数据    allure-results测试数据文件夹（可以更改名字）

# 执行用例并生成allure报告
pytest_ars=['-v','-s','--capture=sys',
            '--clean-alluredir',
            '--alluredir=allure-results',
            './HAT/core/TestRunner.py']

# 执行用例  生成测试数据
pytest.main(pytest_ars)

#生成测试报告  allure-report更改
os.system('allure generate -c -o allure-report')

combine_allure('./allure-report')#会生成一个complete.html可以在c/d盘打开
