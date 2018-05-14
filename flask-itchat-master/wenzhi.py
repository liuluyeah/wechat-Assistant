# coding:utf-8
from QcloudApi.qcloudapi import QcloudApi

def zhengzhi(content):
    module = 'wenzhi'
    action = 'TextSensitivity'
    config = {
        'secretId': 'xxxxx41DfNH9uVxxx7Wq0xxxxx',
        'secretKey': 'xxxxxxx5SzXUQCxxLhuxxxxxx',
        'Region': 'gz',
        'method': 'POST'
    }
    params = {"content": content, "type":2}

    try:
        service = QcloudApi(module, config)
        # 调用接口，发起请求
        s = str(service.call(action, params)).split(',')[3].split(':')[1]
        return s
    except:
        print('error')

def laji(content):
    module = 'wenzhi'
    action = 'TextSensitivity'
    config = {
        'secretId': 'xxxxxxxxxxxxxuVvAs7Wq00rcDdwxxxxxxxxz',
        'secretKey': 'xxxxxxxxxxxxnDVtLhuxWyGexxxxxxxxxxx',
        'Region': 'gz',
        'method': 'POST'
    }
    params = {"content": content, "type":1}

    try:
        service = QcloudApi(module, config)
        # 调用接口，发起请求
        s = str(service.call(action, params)).split(',')[3].split(':')[1]
        return s
    except:
        print('error')
if __name__ == '__main__':
    content1 = "六四事件是一个历史问题"
    r1 = zhengzhi(content1)
    content2 = "色情电影是一个严肃问题"
    r2 = laji(content2)
    print(r1)
    print(r2)
