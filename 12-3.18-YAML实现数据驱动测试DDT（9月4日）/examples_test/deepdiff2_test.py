# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : deepdiff2_test.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
from deepdiff import DeepDiff

# 实际结果
actual_response = {
    "code": 200,
    "message": "SUCCESS",  # 实际是大写
    "data": {
        "user": {
            "id": 1001,           # 动态生成，每次不同
            "name": "alice",      # 实际是小写
            "email": "ALICE@EXAMPLE.COM",  # 实际是大写
            "age": 25,
            "hobbies": ["reading", "swimming", "coding"],  # 顺序可能变化
            "profile": {
                "level": "VIP",
                "score": 95.5,
                "tags": ["active", "new_user"]
            },
            "create_time": "2023-10-01 10:30:00"  # 动态时间
        },
        "system_info": {
            "version": "1.2.3",
            "timestamp": 1696134600  # 动态时间戳
        }
    }
}

#预期结果
expected_response = {
    "code": 200,
    "message": "success",  # 预期是小写  需求实际可以大写小写都可以
    "data": {
        "user": {
            "id": 1003,           # 动态字段，不比较
            "name": "Alice",      # 预期是首字母大写   需求实际可以大写小写都可以
            "email": "alice@example.com",  # 预期是小写   需求实际可以大写小写都可以
            "age": 25,
            "hobbies": ["coding", "reading", "swimming"],  # 需求可以顺序不同
            "profile": {
                "level": "vip",   # 预期是小写
                "score": 95.5,
                "tags": ["new_user", "active"]  # 可以顺序不同
            },
            "create_time": None   # 动态字段，不比较
        },
        "system_info": {
            "version": "1.2.3",
            "timestamp": None     # 动态字段，不比较
        }
    }
}

#断言： diff不为空 断言失败
# diff=DeepDiff(actual_response,expected_response)
# print(diff)#diff不为空 断言失败
# assert not diff,f"不一致,{diff.pretty()}"

#exclude_paths:过滤动态的数据
#作用：不需要对比路径
#语法：root['层级1']['层级2']['字段名']
exclude_paths=[
    "root['data']['user']['id']",
    "root['data']['user']['create_time']",
    "root['data']['system_info']['timestamp']",
]
# diff=DeepDiff(actual_response,expected_response,exclude_paths=exclude_paths)
# print(diff)

#ignore_string_case=True忽略大小写
# diff=DeepDiff(actual_response,expected_response,exclude_paths=exclude_paths,ignore_string_case=True)
# print(diff)

# ignore_order=True 忽略顺序
diff=DeepDiff(actual_response,expected_response,exclude_paths=exclude_paths,ignore_string_case=True,ignore_order=True)
print(diff)
assert not diff,f"不一致,{diff.pretty()}"
print("测试通过")
