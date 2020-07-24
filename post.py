# -*- coding:utf-8 -*-
import requests   #先导入包,这是必须的
import json
def post(Number,body):
    url = ''  # url:接口地址
    data = {
        'phoneNumber': Number,
        'invokeId': '201505121213341300123',
        'sourceSystemId': 'HHOA',
        'sourceServerIp': '192.168.1.108',
        'body': body,
        'remark': '其他业务信息'
    }  # data:接口传递的参数
    j_data = json.dumps(data)
    headers = {}
    headers['Content-Type'] = 'application/json; charset=utf-8'
    # header:传递header信息
    # files:接口中需要上传文件则需要用到该参数
    r = requests.post(url, data=j_data, headers=headers)  # 请求url，获得返回的数据信息
    print("#########")
    print(r)
    print(r.text.encode('utf-8'))  # 获得的返回数据使用text方法进行获取

post("13948290374928","sdfsdf")
