# MXProxyPool
动态代理ip池
## 架构图
![](https://github.com/iamhmx/MXProxyPool/blob/master/screenshots/%E6%9E%B6%E6%9E%84%E5%9B%BE.png?raw=true)

* *说明：爬取模块将会爬取免费代理，免费代理的可用性低，如需获取高效的代理ip，请购买付费代理（[各大付费代理比较](https://cuiqingcai.com/5094.html)）。*

## 安装Python 3.5+
## 安装Redis，并启动服务
```
# mac os安装
pip install redis
# 启动redis
redis-server /usr/local/etc/redis.conf
```
## 安装依赖库
```
cd MXProxyPool
pip install -r requirements.txt
```
## 修改配置
```
settings.py存放了配置信息
```
## 运行代理池
```
cd MXProxyPool
python3 run.py
```
## api接口
```
# 随机获取一个代理
http://localhost:8000/fetch
```
![](https://github.com/iamhmx/MXProxyPool/blob/master/screenshots/api-fetch.png?raw=true)

## 使用代理池示例
```
import requests
from proxypool.settings import API_HOST, API_PORT
from pyquery import PyQuery as pq
import json


def get_one_proxy():
    """
    开启代理池，通过接口，从代理池获取一个代理
    :return: 代理ip
    """
    response = requests.get('http://{}:{}/fetch'.format(API_HOST, API_PORT))
    doc = pq(response.text).text()
    return doc


def test():
    # 不使用代理
    response1 = requests.get('http://httpbin.org/get')
    print(response1.text)
    print('本机ip：', json.loads(response1.text).get('origin'))

    print('='*30 + '使用代理后' + '='*30)
    # 使用代理
    try:
        proxy = {
            'http': 'http://{}'.format(get_one_proxy())
        }
        print('代理ip：', proxy)
        response2 = requests.get('http://httpbin.org/get', proxies=proxy, timeout=15)
        print(response2.text)
        print('本机ip：', json.loads(response2.text).get('origin'))
    except Exception as e:
        print('请求出错', e)
if __name__ == '__main__':
    test()
```