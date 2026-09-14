import jsonpath
import requests

#登录接口
login_url = 'http://shop-xo.hctestedu.com/index.php?s=/api/user/login&application=app&application_client_type=weixin'
login_data = {
    "accounts": "youtian",
    "pwd": "123456",
    "type": "username"
}
try:
    requ = requests.post(login_url, data=login_data)
    login_token = jsonpath.jsonpath(requ.json(), '$..token')[0]
    # print(login_token)
    assert jsonpath.jsonpath(requ.json(),'$..msg')[0] == '登录成功','登陆失败'
except Exception as e:
    raise

# 加入购物车接口

shop_url = f'http://shop-xo.hctestedu.com/index.php?s=/api/cart/save&application=app&application_client_type=weixin&token={login_token}'
shop_data = {
    "goods_id": "2",
    "stock": "3"
}
try:
    requ = requests.post(shop_url,data=shop_data)
    assert jsonpath.jsonpath(requ.json(),'$..msg')[0] == '加入成功','加入失败'
except Exception as e:
    raise


#查看购物车接口

select_shop_url = f'http://shop-xo.hctestedu.com/index.php?s=/api/cart/index&application=app&application_client_type=weixin&token={login_token}'
try:
    requ = requests.post(select_shop_url)
    goods_id = jsonpath.jsonpath(requ.json(),'$..goods_id')[0]
    # print(goods_id)
    assert jsonpath.jsonpath(requ.json(),'$..msg')[0] == 'success','查看购物车失败'
except Exception as e:
    raise



#查看地址列表接口
select_address_url = f'http://shop-xo.hctestedu.com/index.php?s=/api/useraddress/index&application=app&application_client_type=weixin&token={login_token}'
try:
    requ = requests.post(select_address_url)
    address = jsonpath.jsonpath(requ.json(),'$..address')[0]
    # print(address)
    assert jsonpath.jsonpath(requ.json(),'$..msg')[0] == 'success','查看地址失败'
except Exception as e:
    raise

#提交订单接口
add_url = f'http://shop-xo.hctestedu.com/index.php?s=/api/buy/add/index&application=app&application_client_type=weixin&token={login_token}'
data = {
    "buy_type": "goods",
    "goods_id": goods_id,
    "stock": "2",
    "spec": [],
    "address_id": address,
    "payment_id": "3",
    "site_model": 0,
    "user_note": ""
}

try:
    requ = requests.post(add_url,json=data)
    assert jsonpath.jsonpath(requ.json(),'$..msg')[0] == '提交成功','提交订单失败'
except Exception as e:
    raise
print(requ.json())
