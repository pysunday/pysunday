**如有任何问题请及时告知，创作不易感谢支持！**

# pysunday

**pysunday** 是一款基于插件驱动的开发工具包, 旨降低程序员工具开发的复杂度, 目标向集环境、代理、工具等全面的开发框架.

```python
from sunday.core import cmdexec
code, stdout, stderr = cmdexec('ls', 10000)
```

[![Downloads](https://pepy.tech/badge/pysunday/month)](https://pepy.tech/project/pysunday)
[![Supported Versions](https://img.shields.io/pypi/pyversions/pysunday.svg)](https://pypi.org/project/pysunday)
[![Contributors](https://img.shields.io/github/contributors/pysunday/pysunday.svg)](https://github.com/pysunday/pysunday/graphs/contributors)

## 安装

pysunday已在pypi上发布

安装：`python3 -m pip install pysunday`

卸载：`python3 -m pip uninstall pysunday`

更新：`python3 -m pip install --upgrade pysunday`

安装成功后需要执行`python3 -c '__import__("sunday.core.init")'`让sunday自动检查并初始化执行环境, 暂时只支持`zsh`、`bash`的环境初始化

或者手动修改shell的rc文件，添加：

```shell
export SUNDAY_ROOT=~/.sunday
export PATH=$SUNDAY_ROOT/bin:$PATH
```

## Docker安装(试用)

1. 当前目录运行构建image: `docker build -t sunday ./`
2. 以守护进程方式运行启动: `docker run -d --restart always --name sunday -p 5000:5000 -v $HOME/.ssh:/root/.ssh sunday /bin/bash -c 'while true; do echo sunday runing; sleep 10;done'`
3. 执行sunday命令, 如: `docker exec sunday sunday_install https://github.com/pysunday/command-common.git#main`
4. 使用alias设置便捷命令: `echo "alias sunday='docker exec -it sunday'" >> ~/.bashrc; source ~/.bashrc`
5. 运行`sd_getip`命令: `docker exec sunday sd_getip`

## sunday支持及未来支持

[x] 敏捷工具核心库  
[x] 插件化  
[x] 日志系统集成  
[x] 持久化登录态  
[x] 开发环境代理  
[x] 系统PAC支持  
[x] 列表打印  
[x] 多线程运行  
[x] 密文加解密支持  
[ ] LSP多语言支持  
[ ] 开发环境配置  
[ ] UI自动化测试工具  
[ ] 前端辅助开发工具  
[ ] 文档同步wiki  
[ ] 其它功能...

### 正在做的

前端辅助开发工具: 企业级前端项目开发依赖的外部环境太多，往往会影响到前端开发效率，因此该工具希望实现如下功能：

1. 快捷代理，并通过api实现交互，预期使用mitmdump实现
2. 预设场景，根据场景收集与回放接口请求
3. 对收集的数据可版本控制
4. 场景回放支持预设修改

场景化可打通A to B to C最后一公里壁垒，降低项目对开发人员的依赖性

数据代理降低外部环境依赖，如对认证的依赖，hybrid native开发时对壳接口交互的依赖(这个现成mock工具做不到)等

## 插件开发

插件主要指工具插件, 其它配套支持登录插件.

如A开发了一个网站的登录插件, 此后B和C可基于该登录插件开发工具插件

插件必须包含package.json的描述文件, 该文件配置如下:

1. name: 工具名称
2. type: login(登录)/tools(工具)
3. depend: 程序依赖，依赖包git地址的集合
4. keywords: 关键词
5. author: 作者

## 公共配置文件

新建文件`$SUNDAY_ROOT/config.ini`

配置格式如下:

```ini
# config.ini
[NAME1]
key1 = value
key2 = value

[NAME2]
key1 = value
key2 = value
```

### LOGGING

控制日志输出

#### key: level

控制程序日志输出级别, 默认级别为ERROR, 及只输出报错日志

### key: format

日志输出格式控制, 本人使用格式: `format = %%(blue)s[%%(asctime)s.%%(msecs)-3d] %%(log_color)s%%(levelname)-7s: %%(purple)s<%%(name)s> %%(log_color)s%%(message)s`

### PROXY

代理配置, 未设置时, 程序中的请求根据网络配置走系统的pac代理文件, 否则当设置了值后程序中的网络请求不走pac仅走配置的代理

#### key: proxy

配置程序中的请求是否走代理, 代理配置格式如`proxy = 127.0.0.1:8888`

### CRYPTO

加密程序相关配置

#### key=str

key为加密用的密钥, 默认是HOWDUUDU, 可自行修改增加密码安全性

### GIT

GIT相关配置, 如插件安装来源

#### base: git_url_base

配置git地址，当安装的插件或者依赖中的插件不存在git地址则使用该地址

## 内置命令

### `sunday_install`

用于安装sunday插件

```console
uusage: sunday_install [-v] [-h] [--giturl GIT_URL_BASE] [-l] [-N] [MODULE_URLS) [MODULE_URL(S ...]]

安装sunday模块

Positionals:
  MODULE_URL(S)          安装模块的本地模块路径或者仓库名称, 分支请用#字符拼接

Optional:
  -v, --version          当前程序版本
  -h, --help             打印帮助说明
  --giturl GIT_URL_BASE  git元地址, 取配置中的GIT.base字段，未配置则默认为ssh://git@github.com
  -l, --list             打印所有的已安装安装
  -N, --notdepend        是否跳过依赖安装，如果安装本地模块，且依赖的模块也是本地安装则可设置为不安装依赖

使用案例:
    sunday_install sunday/name1.git
    sunday_install https://website.com/sunday/name1.git https://website.com/sunday/name2.git
    sunday_install --giturl https://website.com sunday/name1.git https://website.com/sunday/name2.git sunday/name3.git https://website.com/sunday/name4.git
    sunday_install /path/to/package
```

## 插件收录

### 官方插件

#### command-common

[command-common](https://github.com/pysunday/command-common): 提供好用的命令行命令, 安装: `sunday_install https://github.com/pysunday/command-common.git#main`

命令名 | 来自插件 | 功能 | 是否需要登录
------ | -------- | ---- | ------------
`sd_getip` | common | 查看本机ip | 否
`sd_getport` | common | 查看端口的占用情况 | 否
`sd_chrome` | common | 命令行启动chrome | 否
`sd_grepn` | common | 带行号的命令行搜索，过滤模块包目录、打包目录等 | 否

### tools-imrobot

[tools-imrobot](https://github.com/pysunday/tools-imrobot): 聊天机器人插件, 安装: `sunday_install https://github.com/pysunday/tools-imrobot.git#main`

### login-zhipin

[login-zhipin](https://github.com/pysunday/login-zhipin): zhipin网站登录插件, 安装: `sunday_install https://github.com/pysunday/login-zhipin.git#main`

### tools-zhipin

[tools-zhipin](https://github.com/pysunday/tools-zhipin): zhipin网站智能找工作、智能聊天插件, 安装: `sunday_install https://github.com/pysunday/tools-zhipin.git#main`

### 非官方插件

**多个未收录的企业内部插件稳定运行中**

