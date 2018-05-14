# wechat_analyse

开发环境：pycharm + flask + windows10 + python3

# 数据说明

data.rar为压缩文件，包含80万条垃圾数据，作为垃圾特征提取的数据源

首先，需要在 https://console.qcloud.com/nlp/manage_app.cgi 申请自己的apikey和密钥；

其次，修改wenzhi.py中的apikey和密钥，本文件用来进行语义识别，详情见代码注释；

文智语义接口技术文档详情如下：https://cloud.tencent.com/product/api ,主要用到 Python SDK 已经云 API 接口





# 运行结果

首页http://127.0.0.1:5000/static/index.html：

![首页](https://github.com/liuluyeah/wechat_analyse/blob/master/%E9%A6%96%E9%A1%B5.png)

主页http://127.0.0.1:5000/static/analyse.html：

![主页](https://github.com/liuluyeah/wechat_analyse/blob/master/%E4%B8%BB%E9%A1%B5.png)

![功能页](https://github.com/liuluyeah/wechat_analyse/blob/master/%E5%8A%9F%E8%83%BD%E5%B1%95%E7%A4%BA.png)

# 声明

本软件仅供学习交流，如作他用所承受的法律责任一概与作者无关（下载使用即代表你同意上述观点）

