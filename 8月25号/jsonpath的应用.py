# -*- coding: utf-8 -*-
# jsonpath 练习数据：电商平台订单接口返回示例

import json
import jsonpath

# ============ 复杂 JSON 数据（模拟接口返回） ============
data = {
    "code": 200,
    "message": "success",
    "data": {
        "total": 3,
        "page": 1,
        "orders": [
            {
                "order_id": "20260825001",
                "user": {
                    "id": 101,
                    "name": "张三",
                    "vip_level": 3,
                    "addresses": [
                        {"type": "home", "city": "北京", "detail": "朝阳区xx路1号"},
                        {"type": "work", "city": "北京", "detail": "海淀区yy路2号"}
                    ]
                },
                "items": [
                    {"goods_id": 1001, "name": "苹果手机", "price": 5999, "count": 1},
                    {"goods_id": 1002, "name": "手机壳", "price": 39, "count": 2}
                ],
                "pay_amount": 6077,
                "status": "已发货",
                "create_time": "2026-08-25 10:30:00"
            },
            {
                "order_id": "20260825002",
                "user": {
                    "id": 102,
                    "name": "李四",
                    "vip_level": 1,
                    "addresses": [
                        {"type": "home", "city": "上海", "detail": "浦东新区zz路3号"}
                    ]
                },
                "items": [
                    {"goods_id": 2001, "name": "蓝牙耳机", "price": 299, "count": 1}
                ],
                "pay_amount": 299,
                "status": "待付款",
                "create_time": "2026-08-25 11:00:00"
            },
            {
                "order_id": "20260825003",
                "user": {
                    "id": 101,
                    "name": "张三",
                    "vip_level": 3,
                    "addresses": []
                },
                "items": [
                    {"goods_id": 3001, "name": "机械键盘", "price": 899, "count": 1},
                    {"goods_id": 3002, "name": "鼠标", "price": 199, "count": 1},
                    {"goods_id": 3003, "name": "鼠标垫", "price": 29, "count": 3}
                ],
                "pay_amount": 1185,
                "status": "已完成",
                "create_time": "2026-08-24 20:00:00"
            }
        ],
        "summary": {
            "order_count": 3,
            "total_amount": 7561,
            "vip_user_count": 2,
            "city": ["北京", "上海"]
        }
    }
}


# ============ jsonpath 练习题（自己动手写表达式，没有答案） ============
# 提示语法：
#   $             根节点
#   .             下一级
#   ..            深层查找（跨层级）
#   [index]       数组下标，从 0 开始
#   [?(@.xxx==值)] 条件过滤

# 题目1：提取所有订单号（用深层查找 ..）
dingdan = jsonpath.jsonpath(data,'$..order_id')[0]
print(dingdan)

# 题目2：提取第一个订单的用户名（用下标 [0]）
# 题目3：提取所有商品名称（跨层级 ..）
# 题目4：提取所有商品价格
# 题目5：提取所有用户 id（注意：用户 id 会重复出现）
# 题目6：提取所有出现过的城市（地址里的 + summary 里的）
# 题目7：提取状态为"已完成"的订单（用条件过滤）
# 题目8：提取支付金额大于 500 的订单的 pay_amount
# 题目9：提取第三个订单里第一个商品的名称
# 题目10：提取张三（id=101）的所有订单号
# 题目11：提取所有 vip_level 大于 1 的用户名
# 题目12：提取所有订单的 create_time
