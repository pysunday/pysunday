# API-接口请求

封装requests，会话控制与接口交互管理

---

## API说明

写python大家都会用requests发起请求，但是对于复杂的情况，直接用requests就会显得很复杂，比如：内网环境使用系统pac代理、保持会话、请求失败再次尝试、请求代理等，这些都是数据采集开发中常常遇到的问题，使用PYSunday的Fetch API来开发网页接口数据请求可以不用考虑这些问题

::: sunday.core.fetch.Fetch
    :docstring:
    :members: add_header get post get_json post_json getCookiesDict setCookie setJsonError

NOTE: **提示**
每个Fetch实例都是一个会话，如果同网站涉及cookie的请求请使用同一个Fetch实例

## 示例

### 1. 模拟多个客户端发起请求

通过设置代理和请求头的`User-Agent`值模拟不同的客户端，如下：

```python
from sunday.core.fetch import Fetch

client = Fetch(proxy='101.102.103.104:8888')
client.add_header({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
  })
print(client.get_json('http://httpbin.org/get'))
"""
{
  'args': {},
  'headers': {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Host': 'httpbin.org',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
    'X-Amzn-Trace-Id': 'Root=1-63db4b51-2de83d893867d9636863e056'
  },
  'origin': '101.102.103.104',
  'url': 'http://httpbin.org/get',
}
"""
```

### 2. 设置超时时间及重试次数

```python
from sunday.core.fetch import Fetch

fetch = Fetch()
fetch.get('http://www.baidu.com', timeout=60, timeout_time=10)
```
