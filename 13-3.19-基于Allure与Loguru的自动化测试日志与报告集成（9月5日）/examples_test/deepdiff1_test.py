# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : deepdiff1_test.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
from deepdiff import DeepDiff

# exmsg={"name":"alice","age":25}
# sjmsg={"name":"alice","age":25}
# diff=DeepDiff(exmsg,sjmsg)
# print(diff)
#输出的结构
#有差异：返回差异类型  values_changed  missing_key缺失字段。。。差异路径+具体值
#没有差异：返回空字典{}


exmsg={"name":"alice","age":25}
sjmsg={"name":"Alice","age":25}
diff=DeepDiff(exmsg,sjmsg)
print(diff)
assert not diff,f"不一致,{diff.pretty()}"


#not DeepDiff
# {} 证明用例通过
#有数据 用例不通过

# assert not diff,f"不一致,{diff.pretty()}"
#当diff为空时断言通过
#当diff有数据：not {"values_changed":....}断言失败
#diff.pretty() 输出错误信息