"""
接口流程实战（教学版调用方式 + 英文命名）

流程：登录 -> 加入购物车 -> 查看购物车 -> 查看地址 -> 提交订单
使用 api_client.py 的二次封装，try/except 已封装在内部，调用处只保留断言
"""

import jsonpath
import requests

from api_client import ApiClient

client = ApiClient(requests)  # 传 requests 模块；如需保持会话可传 requests.session()

# ============ 1. 登录接口 ============
login_url = 'http://shop-xo.hctestedu.com/index.php?s=/api/user/login&application=app&application_client_type=weixin'
login_data = {
    "accounts": "youtian",
    "pwd": "123456",
    "type": "username"
}
login_response = client.send_post(url=login_url, data=login_data)
login_token = jsonpath.jsonpath(login_response.json(), '$..token')[0]
assert jsonpath.jsonpath(login_response.json(), '$..msg')[0] == '登录成功', '登录失败'

# ============ 2. 加入购物车接口 ============
cart_url = f'http://shop-xo.hctestedu.com/index.php?s=/api/cart/save&application=app&application_client_type=weixin&token={login_token}'
cart_data = {
    "goods_id": "2",
    "stock": "3"
}
cart_response = client.send_post(url=cart_url, data=cart_data, data_type='json')
assert jsonpath.jsonpath(cart_response.json(), '$..msg')[0] == '加入成功', '加入购物车失败'

# ============ 3. 查看购物车接口（取 goods_id） ============
cart_index_url = f'http://shop-xo.hctestedu.com/index.php?s=/api/cart/index&application=app&application_client_type=weixin&token={login_token}'
cart_index_response = client.send_get(url=cart_index_url)
goods_id = jsonpath.jsonpath(cart_index_response.json(), '$..goods_id')[0]
assert jsonpath.jsonpath(cart_index_response.json(), '$..msg')[0] == 'success', '查看购物车失败'

# ============ 4. 查看地址列表接口（取 address） ============
address_url = f'http://shop-xo.hctestedu.com/index.php?s=/api/useraddress/index&application=app&application_client_type=weixin&token={login_token}'
address_response = client.send_post(url=address_url)
address = jsonpath.jsonpath(address_response.json(), '$..address')[0]
assert jsonpath.jsonpath(address_response.json(), '$..msg')[0] == 'success', '查看地址失败'

# ============ 5. 提交订单接口 ============
order_url = f'http://shop-xo.hctestedu.com/index.php?s=/api/buy/add/index&application=app&application_client_type=weixin&token={login_token}'
order_data = {
    "buy_type": "goods",
    "goods_id": goods_id,
    "stock": "2",
    "spec": [],
    "address_id": address,
    "payment_id": "3",
    "site_model": 0,
    "user_note": ""
}
order_response = client.send_post(url=order_url, data=order_data, data_type='json')
assert jsonpath.jsonpath(order_response.json(), '$..msg')[0] == '提交成功', '提交订单失败'

print(order_response.json())
