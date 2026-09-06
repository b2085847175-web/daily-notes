# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : allure_step_logger.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import io
from contextlib import contextmanager

import allure
from loguru import logger


#创建一个日志器
class StepLogCollector:
    #准备工作
    def __init__(self):
        self.log_buffer=io.StringIO()#笔记本
        self.sink_id=None #笔记本的id

    #记入内容
    def __enter__(self):
        self.sink_id = logger.add(self.log_buffer, level="DEBUG")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.remove(self.sink_id)
        log_content=self.log_buffer.getvalue()#读取笔记本内容
        if log_content.strip():#避免空日志 把内容加入到allure报告
            allure.attach(
                log_content,
                name="步骤日志",
                attachment_type=allure.attachment_type.TEXT
            )
        self.log_buffer.close()



#支持with的语法  allure步骤+日志收集
@contextmanager
def allure_step_with_log(step_name):#用例步骤
    with allure.step(step_name):#进入发送请求post
        with StepLogCollector() as collector:  #日志收集
            yield collector #暂停执行，执行步骤内的代码

