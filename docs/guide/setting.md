# PYSunday 配置

全局配置控制插件行为

---

## 运行目录

安装成功后，程序默认会将`~/.sunday`作为程序运行目录，可以通过运行`python3 -c '__import__("sunday.core.init")'`自助配置，配置成功后环境变量会新增运行路径键`SUNDAY_ROOT`，`PATH`环境变量头部新增目录`.sunday/bin`，可如下查看程序运行目录：

```bash
$ echo $SUNDAY_ROOT
/Users/rnet/.sunday
```

初始情况下运行目录中只有bin目录，用于存放PYSunday自带的可执行命令

安装插件并执行相关命令后一般会出现如下目录及文件：

```markdown
$ ls $SUNDAY_ROOT
bin/              config.ini       module-lock.json
cache/            log/             plugins/
```

WARNING: **注意:**
其中config.ini是程序配置文件，并不是程序自动生成的，后面会做说明。

### bin目录

bin目录放置的都是基于PYSunday的可执行文件，如自带的`sunday_install`命令、命令插件`package.json`中`bin`字段指定的可执行文件在插件安装成功后也会在这个目录里出现，该目录下的文件都可以在命令行中任何目录下执行.

### plugins目录

顾名思义，该目录存放安装的pysunday插件，其中`branch@user+name`为从git仓库拉取的插件，如：

```markdown
$ ls
command-common            tools-chanjet             tools-imrebot
login-avms                tools-chinagkong          tools-ocr
login-chanjet             tools-chinamecha          tools-proxy
login-elk                 tools-driver              tools-rebot
login-etax                tools-elk                 tools-taxbill
login-zhipin              tools-etax                tools-taxpayer
main@pysunday+tools-proxy tools-gmz                 tools-taxtype
tools-huicong             tools-haodf               tools-zhipin
tools-baoshui
```

### log目录

log目录存放程序日志文件。

NOTE: **提示**
基于PYSunday的插件执行结束后会在尾部打印程序执行时间及日志存储目录，如：  
[11:40:43.86 ] INFO   : <SUNDAY> program execution time 1117810.41 s  
[11:40:43.106] INFO   : <SUNDAY> LOG FILE AT: /Users/rnet/.sunday/log/2023-01-18T13:10:32.646701

WARNING: **注意**
该目录的文件都是程序执行的日志文件，在程序执行后可用于运行分析，PYSunday不会主动删除日志文件，因此有可能需要使用者手动清理无用日志文件

### cache目录

cache目录存放的是程序中需要缓存的文件，如登录插件缓存的用户输入数据及登录态数据

### module-lock.json文件

该文件为PYSunday安装插件后自动生成，用于记录插件的关键数据。

## PYSunday全局配置文件config.ini

该文件非必须，用户可以通过该文件个性化配置PYSunday的部分行为。

PYSunday运行会读取`$SUNDAY_ROOT/config.ini`文件内的配置项，可以控制日志、登录、加密解密、代理等行为，如作者样例：

```text
[LOGGING]
level  = DEBUG
format = %%(blue)s[%%(asctime)s.%%(msecs)-3d] %%(log_color)s%%(levelname)-7s: %%(purple)s<%%(name)s> %%(log_color)s%%(message)s
print_file = True

[LOGIN]
cookieFile = .cookies
envFile    = .env

[CRYPTO]
key = 'gmzgmz_123456_gmzgmz'

[PROXY]
proxy = 127.0.0.1:8888
```

### LOGGING

控制日志输出

1. level: 控制程序日志输出级别, 默认级别为ERROR, 及只输出报错日志
2. format: 日志输出格式控制
3. print_file: 是否打印日志缓存文件
4. write_file(待实现): 是否写入日志到缓存文件

NOTE: **提示**
插件命令运行时的`--loglevel`优先级大于全局配置的level，因此开发时可将level设置为DEBUG，
命令执行时再按需要修改

### PROXY

代理配置, 未设置时, 程序中的请求根据网络配置走系统的pac代理文件, 否则当设置了值后程序中的网络请求不走pac仅走配置的代理

1. proxy: 配置程序中的请求是否走代理, 代理配置格式如`proxy = 127.0.0.1:8888`

### CRYPTO

加密程序相关配置

1. key: 配置加解密用的密钥, 默认是`HOWDUUDU`, 可自行修改增加密码安全性

### GIT

GIT相关配置, 如插件安装来源

1. base: 配置git地址，当安装的插件或者依赖中的插件不存在git地址则使用该地址

### LOGIN

登录插件相关配置

1. cookieFile: 登录态缓存文件名，默认为`.cookies`
2. envFile: 登录输入参数缓存文件名, 默认为`.env`
