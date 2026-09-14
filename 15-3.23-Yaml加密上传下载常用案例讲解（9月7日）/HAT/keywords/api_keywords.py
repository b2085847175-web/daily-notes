# -*- coding: utf-8 -*-
# @Author  : 柚一
# @File    : requests二次封装.py
# https://pypi.tuna.tsinghua.edu.cn/simple/
# 项目地址可能发生变化，测试数据如果太多可能随时还原。 碰到地址打不开，报错等等情况，联系班主任老师及时反馈
import base64
import os
import sys

import allure
import jsonpath
import pymysql
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from deepdiff import DeepDiff
from loguru import logger
from pymysql import cursors

from HAT.core.globalContext import g_context


#封装的好处：每次要用的时候，直接调用这个函数，更改的时候只要更改这个函数即可
# 一处修改，处处生效
class Keywords:
    # request传requests /requests.session
    def __init__(self,request):
        self.request=request

    #参数不能写死  python **kwargs 接受很多关键字参数
    @allure.step("发送请求POST")
    def 发送请求POST(self,**kwargs):
        self.show_log("请求参数", kwargs)
        url=kwargs.get("请求地址",None)#没获取到地址给个None  http://shop-xo.hctestedu.com/index.php?s=/api/user/login&application=app&application_client_type=weixin
        data=kwargs.get("请求数据",None) #{"accounts": "youtian", "pwd": "123456","type": "username"}
        params=kwargs.get("URL参数",None)
        headers=kwargs.get("请求头",None)
        files=kwargs.get("文件列表",[])
        data_type=kwargs.get("请求类型","data").lower()#默认请求数据类型  取决于content-type

        # 构造统一的请求参数字典  requests.post(**requests_data)
        requests_data={
            "url":url,
            "params":params,
            "headers":headers,
            "files":files,
        }

        #区分传参类型（json传参还是 data传参）
        if data_type=='json':
            requests_data["json"]=data
        elif data_type=="data":
            requests_data["data"] = data
        elif data_type=="files":#接受到你的参数是files类型
            if isinstance(data,dict):#判断你的数据是不是字典
                files={}
                #key image
                #file_path  路径
                for key,file_path in data.items():
                    files[key]=open(file_path,"rb")
                requests_data["files"]=files #files={"image":open(file_path,"rb")}
            else:#不是字典
                file=open(data,"rb")
                requests_data["files"]={"file":file}

        else:
            raise Exception("请求类型错误，仅支持json/data")

        #发送请求+异常处理  requests.request("post",**requests_data)==requests.post(url,params=params,json=xxx)
        try:
            response=self.request.request("post",**requests_data)
            print("发送结果",response.json())

            g_context().set_dict("响应结果",response) #把返回结果放在全局变量
            logger.info("发送了请求")
            return response
        except Exception as e:
            logger.error("发送请求有问题")
            raise


    def 下载接口get(self,**kwargs):
        url = kwargs.get('请求地址', None)
        params = kwargs.get('URL参数', None)
        headers = kwargs.get('请求头', None)
        data = kwargs.get('请求数据', None)
        files = kwargs.get('文件列表', [])
        save_path=kwargs.get("保存路径")
        stream=kwargs.get("流式下载",False)
        chunk_size=kwargs.get("块大小",1024)
        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "files": files,
            "stream":stream if save_path else False
        }

        response = self.request.request("get", **request_data)
        if save_path:#如果有保存路径的值
            #如果文件不存在就创建，文件存在不报错
            os.makedirs(os.path.dirname(save_path),exist_ok=True)
            if stream:
                #如果是大文件，把文件切割成小文件进行保存
                with open(save_path,"wb") as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
            else:#不是大文件就正常保存
                with open(save_path,"wb") as f:
                    f.write(response.content)
        return response


    @allure.step("发送请求GET")
    def 发送请求GET(self,**kwargs):
        url = kwargs.get('请求地址', None)
        params = kwargs.get('URL参数', None)
        headers = kwargs.get('请求头', None)
        data = kwargs.get('请求数据', None)
        files = kwargs.get('文件列表', [])
        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "files": files,
        }
        response = self.request.request("get", **request_data)
        return response

    @allure.step("提取数据JSON")
    def 提取数据JSON(self,**kwargs):
        self.show_log("提取json数据",kwargs)
        EXPRESSION=kwargs.get("表达式",None) #$.token

        INDEX=kwargs.get("下标",None)#取到很多值的时候，你自己给个你想要提取哪个值的下标  默认取第一值
        if INDEX is None:
            INDEX=0

        response=g_context().get_dict("响应结果").json()
        result=jsonpath.jsonpath(response, EXPRESSION)
        if not result:
            raise Exception(f"没有找到对应的数据:{EXPRESSION}")
        ex_data=result[INDEX]  #具体取到你要的数据

        g_context().set_dict(kwargs["变量名"],ex_data)
        print("全局变量中有没token值",g_context().show_dict())

    @allure.step("断言文本")
    def 断言文本(self,**kwargs):
        #比较器  == !=
        comparators={
            "==":lambda a,b:a==b,
            ">=":lambda a,b:a>=b,
            "<=": lambda a, b: a <= b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            "in": lambda a, b: a in b,
        }

        message=kwargs.get("错误信息",None)#用例有没有传错误信息
        operators=kwargs.get("比较符",'==')#用例有没有传比较符  没有传默认==
        compare_type=kwargs.get("断言类型","文本")#用例有没有传断言类型，没有就默认文本

        #判断你传过来的比较符在不在比较器里面，不在就报错
        if operators not in comparators:
            raise Exception(f"没有对应的比较符{operators}")

        #如果你传过来的是数字，把期望结果转成数字
        if compare_type=="数字":
            kwargs["期望结果"]=float(kwargs["期望结果"])
        else:
            kwargs["期望结果"] = str(kwargs["期望结果"])

        #预期结果和实际结果的对比
        #if not  True ==false      登陆成功 == 登陆成功    if false 不进入判断  没有任何提示  断言成功
        # if not  False== True == 登陆成功 用户名或密码错误  if true 进入判断：
        # 2<  1
        if not comparators[operators](kwargs["实际结果"],kwargs["期望结果"]):
            if message: #登陆错误
                raise Exception(message)
            else: #登陆成功==用户名或密码错误 失败
                raise Exception(f"{kwargs['实际结果']} {operators} {kwargs['期望结果']}失败")

    def 断言文本相等(self,**kwargs):
        kwargs.update({"比较符":"=="})
        self.断言文本(**kwargs)

    def 断言文本不相等(self,**kwargs):
        kwargs.update({"比较符":"!="})
        self.断言文本(**kwargs)

    def 断言文本包含(self, **kwargs):
        kwargs.update({"比较符": "in"})
        self.断言文本(**kwargs)

    def 断言数字相等(self, **kwargs):
        kwargs.update({"比较符": "==","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字大于等于(self, **kwargs):
        kwargs.update({"比较符": ">=","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字小于等于(self, **kwargs):
        kwargs.update({"比较符": "<=","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字不等于(self, **kwargs):
        kwargs.update({"比较符": "!=","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字小于(self, **kwargs):
        kwargs.update({"比较符": "<","断言类型":"数字"})
        self.断言文本(**kwargs)

    def 断言数字大于(self, **kwargs):
        kwargs.update({"比较符": ">","断言类型":"数字"})
        self.断言文本(**kwargs)


    def 批量断言(self,**kwargs):
        try:
            exmsg=kwargs["期望结果"]
            #从全局变量拿到实际结果
            sjmsg=g_context().get_dict("响应结果").json()
            exclude_paths=kwargs.get("过滤字段",[])
            ignore_string_case=kwargs.get("忽略大小写",True)#没传值就是默认忽略大小写
            ignore_order=kwargs.get("忽略顺序",True)#没传值就是默认忽略顺序

            screen_data={
                "exclude_paths":exclude_paths,
                "ignore_string_case":ignore_string_case,
                "ignore_order":ignore_order
            }
            diff=DeepDiff(sjmsg,exmsg,**screen_data)
        except Exception as e:
            assert False,f"批量断言失败,{e}"
        assert not diff,f"批量断言失败{diff.pretty()}"


    def 提取数据库MYSQL(self,**kwargs):
        results={}
        # 1.连接数据库  数据库信息不能写死  放在context.yaml  放在了全局变量  从全局变量中取数据
        db_config=g_context().get_dict("_数据库")[kwargs["数据库"]]
        config = {"cursorclass": cursors.DictCursor}
        config.update(db_config)
        #连接数据库
        connect = pymysql.connect(**config)
        # 2.创建游标
        cursor = connect.cursor()
        # 3.写sql语句
        sql = kwargs["SQL"]
        # 4.游标执行sql语句
        cursor.execute(sql)
        # 5.游标获得结果
        rs = cursor.fetchall()
        print(rs)
        # 6.游标关闭
        cursor.close()
        # 7.数据库连接关闭
        connect.close()

        #结果保存在变量中  保存在变量中为了后面方便使用
        var_names=kwargs.get("变量名",[])

        #判断你有没有写变量名
        # 如果写了变量名 {'id': 2, 'username': 'youyi'},{'id': 3, 'username': 'youer'}   [uid,uname]  uid_1:2 uname_1:youyi    uid_2:3 uname_2:youer
        #如果没写变量名 {'id': 2, 'username': 'youyi'},{'id': 3, 'username': 'youer'}     id_1:2 username_1:youyi    id_2:3 username_2:youer
        if not var_names: #没有变量名
            #i=1  item={'id': 2, 'username': 'youyi'}  {id_1:2 username_1:youyi}
            for i,item in enumerate(rs,start=1):
                for key,value in item.items():
                    results[f"{key}_{i}"]=value  #results[id_1]=2 result={id_1:2,username_1=youyi}
        else:
            field=len(rs[0]) if rs else 0
            if len(var_names)!=field:
                raise Exception(f"变量名数量和结果数量不一致{var_names}")

            #idx=1 item={'id': 2, 'username': 'youyi'}
            for idx,item in enumerate(rs,start=1):
                for col_idx,key in enumerate(item):#col_idx=0,key=id  col_idx=1 key=username
                    results[f"{var_names[col_idx]}_{idx}"] = item[key]  #results[uid_1]=2  {uid_1:2}  results[uname_1]=youyi

        g_context().set_by_dict(results)
        print("数据库结果保存在变量中",g_context().show_dict())


    def show_log(self,data_name,data=None):
        logger.debug(f"-------Log：{data_name}-----")
        logger.debug(f"{data_name}:{data}")
        logger.debug(f"-------END Log：{data_name}-----")

    #     没有找到请求方法的时候，来这个这个ex_invoke方法
    def ex_invoke(self,**kwargs):
        key=kwargs['key']#key是什么内容，找什么文件名，拿到发送请求post
        if g_context().get_dict("key_dir") is not None:
            sys.path.append(g_context().get_dict("key_dir"))#找目录文件
            module=__import__(key)#导入模块
            class_=getattr(module,key)#获取模块中的方法
            key_func=class_(requests).__getattribute__(key)
            key_func(**kwargs['step_value'])


    def 加密aes(self,**kwargs):
        key = b'1234567812345678'
        # 加密数据
        data = kwargs['data'].encode('utf-8')
        # 加密ECB
        cipher = AES.new(key, AES.MODE_ECB)
        # 填充数据
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        #加密好的数据放在全局变量
        g_context().set_dict(kwargs['VARNAME'],ct)
        print("全局变量数据", g_context().show_dict())