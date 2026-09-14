# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : 加密数据.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

#密钥  约定好的密钥
key=b'1234567812345678'
#加密数据
data='123456'
#aes需要字节数据
data=data.encode('utf-8')
#加密ECB
cipher=AES.new(key,AES.MODE_ECB)
#填充数据
ct_bytes=cipher.encrypt(pad(data,AES.block_size))
ct=base64.b64encode(ct_bytes).decode('utf-8')
print("加密数据",ct)


#加密：密码   123  字符串123456 数字 23
#解密：数字--字符串--密码

#解密
ci_bytest=base64.b64decode(ct)
cipher=AES.new(key,AES.MODE_ECB)
pt=unpad(cipher.decrypt(ci_bytest),AES.block_size)
c=pt.decode("utf-8")
print("解密数据",c)
