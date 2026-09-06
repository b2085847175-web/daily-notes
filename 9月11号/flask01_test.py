# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : flask01_test.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈

#简单接口  搜索的接口
from flask import Flask, request

# 2. 创建应用实例（固定写法，不要改）
app = Flask(__name__)

# 3. 定义接口路由（URL + 请求方式）  不写请求方式，就是默认get请求
# @app.route('/list')
# def mock_test():
#     # 4. 写接口逻辑，返回假数据
#     return "列表查询成功"



# @app.route('/list',methods=['get'])
# def mock_test():
#     # 4. 写接口逻辑，返回假数据
#     return "首页列表查询成功"


# @app.route('/api/pay',methods=['POST'])
# def pay():
#     # 4. 写接口逻辑，返回假数据
#     return "支付成功"


# get请求参数获取
# @app.route('/list',methods=['get'])
# def mock_test():
#     # res=request.args
#     # print("获取所有数据",res) #获取的ImmutableMultiDict([('id', '2')])
#     # res = request.args.to_dict()
#     # print("获取所有数据", res)#自动数据，方便取值 {'id': '2'}
#     # res = request.args.get("id")
#     # print("获取所有数据", res)#获取所有数据 2
#     print("请求头",request.headers)
#     print("请求方式",request.method)
#     print("请求地址",request.url)
#     return "首页列表查询成功"


# post传参获取
@app.route('/login',methods=['post'])
def mock_test():
    # res=request.data
    # res=request.get_data()
    # print("获取二进制数据",res)
    #json数据
    # res = request.json
    res = request.get_json()
    print("获取json数据", res)
    return "你好"




# 5. 启动服务
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)

#debug=True：代码修改后自动重启  保存一下
# http://127.0.0.1:8888/login