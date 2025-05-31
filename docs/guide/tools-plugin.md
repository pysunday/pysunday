# 工具插件开发

快速开发工具插件，如命令行工具命令、后端功能服务、爬虫应用等。

---
## 介绍


## 插件讲解

模版仓库地址：https://github.com/pysunday-plugins/tools-template

文件结构如下：

```
.
├── __init__.py
├── package.json
├── README.md
├── requirements.txt
└── sunday_template.py
```

### requirements.txt

此处存放插件依赖的第三方包，执行sunday_install命令后会自动安装

### package.json

用于存放项目的基本信息

模版插件package.json内容如下：

```json
{
  "name": "template",
  "type": "tools",
  "version": "1.0.0",
  "description": "样例工具",
  "bin": ["sunday_template"],
  "depend": ["pysunday-plugins/login-template"],
  "keywords": [
    "sunday",
    "tools"
  ],
  "author": "pysunday"
}
```

键名 | 介绍 | 类型 | 默认值
---- | ---- | ---- | ------
name | 插件名称 | str | - 
type | 插件类型 | `tools/login` | tools
version | 版本号 | str | -
description | 插件描述 | str | -
bin | 命令行可执行命令 | list | -
depend | 依赖的插件 | list | -
keywords | 关键词 | list |  -
author | 作者 | str | -

其中type区分是登录插件还是工具插件，配合name的值，最终会生成名为tools-name的文件夹

bin放置的是命令行命令，安装后最终会放入PySunday的可执行命令目录中

depend存放的依赖的插件，会自动从github中找到插件并自动安装

### 命令主体代码

```python
# coding: utf-8 import json
import pprint
from sunday.core import getConfig, getParser
from sunday.login.template import getLoginHandler

CMDINFO = {
    "version": '0.0.1',
    "description": "命令行工具",
    "epilog": "",
    'params': {
        'DEFAULT': [
            {
                'name': ['-m', '--mobile'],
                'help': '手机号',
                'dest': 'mobile',
                'required': True,
            },
            {
                'name': ['-p', '--pass'],
                'help': '密码',
                'dest': 'password',
            },
        ],
    }
}

cryptoKey = getConfig('CRYPTO')('key')

class Template():
    def __init__(self, mobile=None, password=None, *args, **kwargs):
        self.mobile = mobile
        self.password = password

    def getData(self):
        loginer = getLoginHandler('TemplateLogin')(
                phone=self.mobile,
                password=self.password).login()
        data = loginer.rs.get_json('https://target.site')
        if data.get('stat') != 1: return
        return data

    def console(self, data):
        pprint.pprint(data)

    def run(self, isCmd=False):
        ans = self.getData()
        if isCmd:
            self.console(ans)
        else:
            return ans


def runcmd():
    parser = getParser(**CMDINFO)
    handle = parser.parse_args(namespace=Template())
    handle.run(True)

if __name__ == "__main__":
    runcmd()
```

可以看到首先定义了CMDINFO变量，用于定义命令的入参及-h帮助命令的显示内容，最终通过getParser方法生成入参集成对象

获得完整代码：`handle = getParser(**CMDINFO).parse_args(namespace=Template())`

方法runcmd是每个工具插件必须的，用于和类对象功能分离和封装，因此类对象也可以应用于其它python代码中，如后端服务等。

## 安装与应用

1. 开发完后使用命令`sunday_install tools-template`安装该插件
2. 其它python代码也可以用我们前面定义的功能类：`from sunday.tools.template import Template`

安装成功后即可以使用-h查看该工具使用方法：`sunday_template -h`

```bash
❯ sunday_template -h
usage: sunday_template -m MOBILE [-p PASSWORD] [-v] [-h] [--loglevel LEVEL]

命令行工具

Optional:
  -m MOBILE, --mobile MOBILE    手机号
  -p PASSWORD, --pass PASSWORD  密码
  -v, --version                 当前程序版本
  -h, --help                    打印帮助说明
  --loglevel LEVEL              日志等级（debug、info、warning、error、critical）, 默认debug
```

## 参考已有项目

点击下面项目名称查看，或者点击[PySunday tools](https://github.com/orgs/pysunday-plugins/repositories?q=tools)查看其它登录插件

1. [avms自动打包+发布工具](https://github.com/pysunday-plugins/tools-avms)
2. [代理辅助工具](https://github.com/pysunday-plugins/tools-proxy)
3. [BOSS直聘自动聊天工具](https://github.com/pysunday-plugins/tools-zhipin)
