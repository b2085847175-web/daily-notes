import os

import pytest
from allure_combine import combine_allure

pytest_ars = [
    '-v',
    '-s',
    '--capture=sys',
    '--clean-alluredir',
    '--alluredir=allure-results',
    './HAT/core/testrun.py'
]

pytest.main(pytest_ars)

os.system('allure generate -c -o allure-report')

combine_allure('./allure-report')
