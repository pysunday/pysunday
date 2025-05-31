# 创建插件

命令行方式创建PySunday项目

---
通过内置的命令行命令`sunday_create`创建PySunday项目。

模版仓库地址：

* **tools**：https://github.com/pysunday-plugins/tools-template
* **login**：https://github.com/pysunday-plugins/login-template

## 使用方法

```bash
❯ sunday_create -h
usage: sunday_create [-t PTYPE] [-n PNAME] [-v] [-h] [--loglevel LEVEL]

创建PySunday项目

Optional:
  -t PTYPE, --type PTYPE  项目类型，登录: l/login，工具: t/tools
  -n PNAME, --name PNAME  项目名称
  -v, --version           当前程序版本
  -h, --help              打印帮助说明
  --loglevel LEVEL        日志等级（debug、info、warning、error、critical）, 默认debug

使用案例:
    sunday_create
    sunday_create -t tools -n myproject
```

命令`sunday_create -t tools -n myproject`等同于`git clone https://github.com/pysunday-plugins/tools-template.git myproject`
