# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : flask01_test.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈

# mock主要写假接口，返回数据，正常的数据异常数据
# 登陆的接口，输入正确的用户名和密码返回登陆成功
# 登陆的接口，输入正确的用户名和错误的密码返回登陆失败
# 问题，我怎么知道输入的用户名和密码是正确的还是错误？
# 项目中 （用户输入用户名和密码） 数据给到数据库  数据库早就存好了用户注册号的数据
#提前准备好数据

#简单接口  搜索的接口
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#登陆成功
MSG_LOGIN_SUCCESS = {'msg': '登录成功', 'code': 0, 'data': {'id': '2', 'username': 'youyi', 'nickname': '', 'mobile': '', 'email': '', 'avatar': 'http://shop-xo.hctestedu.com/static/upload/images/user_avatar/compr/2025/07/05/202507051618191471059059.jpg', 'alipay_openid': '', 'weixin_openid': '', 'weixin_unionid': '', 'weixin_web_openid': '', 'baidu_openid': '', 'toutiao_openid': '', 'qq_openid': '', 'qq_unionid': '', 'integral': '0', 'locking_integral': '0', 'referrer': '0', 'add_time': '1750923161', 'add_time_text': '2025-06-26 15:32:41', 'mobile_security': '', 'email_security': '', 'user_name_view': 'youyi', 'is_mandatory_bind_mobile': 0, 'token': '2c36bd0e1ca6c0c5347be94dfa446bb6'}}

#用户名或者密码错误
USERNAME_OR_PASSWORD_ERROR = {'msg': '用户名或者密码错误', 'code': 10001, 'data': None}

#用户名或者密码不能为空
NOT_NULL = {'msg': '用户名或者密码不能为空', 'code': 10001, 'data': None}

fail = {'msg': '失败', 'code': 10001, 'data': None}

# 早就存好了用户注册号的数据
all_user={"username":"youyi","password":"123456"}

# post传参获取
@app.route('/login',methods=['post'])
def mock_test():
    #获取用户参数
    res = request.get_json()
    print("获取json数据", res)
    # 用户名和密码拿出来
    username=res["username"]#youyi
    password=res["password"]#1234566

    #判断
    if username==all_user["username"] and password==all_user["password"]:
        return jsonify(MSG_LOGIN_SUCCESS)#jsonify把字典转成标准的json格式返回给前端
    elif username=="" or password=="":
        return jsonify(NOT_NULL)
    elif username!=all_user["username"] or password!=all_user["password"]:
        return jsonify(USERNAME_OR_PASSWORD_ERROR)
    else:
        return jsonify(fail)




# 5. 启动服务
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)

#debug=True：代码修改后自动重启  保存一下
# http://127.0.0.1:8888/login