# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : mysql_test.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
# python操作数据库
# 1.连接数据库
# 2.创建游标（类似鼠标 执行sql语句 获得结果）
# 3.写sql语句
# 4.游标执行sql语句
# 5.游标获得结果
# 6.游标关闭
# 7.数据库连接关闭
import pymysql
from pymysql import cursors

# 1.连接数据库
connect=pymysql.connect(host="shop-xo.hctestedu.com",
                port=3306,
                user="api_test",
                password="Aa9999!",
                db="shopxo_hctested",
                cursorclass=cursors.DictCursor,#数据以字典方式展示
                charset='utf8'
                )

# 2.创建游标
cursor=connect.cursor()

# 3.写sql语句
sql="select id,username from sxo_user where username='youyi'"

# 4.游标执行sql语句
cursor.execute(sql)

# 5.游标获得结果
rs=cursor.fetchall()
print(rs)

# 6.游标关闭
cursor.close()
# 7.数据库连接关闭
connect.close()