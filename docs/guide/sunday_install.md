# 安装PySunday插件

PySunday的核心工具，用于安装插件。

---

工具类插件需将命令放于package.json文件的bin键中。

该工具可以安装本地插件和github等git托管工具上的插件。

## 使用方法

```bash
❯ sunday_install -h
usage: sunday_install [-v] [-h] [--loglevel LEVEL] [--giturl GIT_URL_BASE] [-l] [-N] [MODULE_URL(S) ...]

安装sunday模块

Positionals:
  MODULE_URL(S)          安装模块的本地模块路径或者仓库名称, 分支请用#字符拼接

Optional:
  -v, --version          当前程序版本
  -h, --help             打印帮助说明
  --loglevel LEVEL       日志等级（debug、info、warning、error、critical）, 默认debug
  --giturl GIT_URL_BASE  git元地址, 取配置中的GIT.base字段，未配置则默认为ssh://git@github.com
  -l, --list             打印所有的已安装安装
  -N, --notdepend        是否跳过依赖安装，如果安装本地模块，且依赖的模块也是本地安装则可设置为不安装依赖

使用案例:
    sunday_install sunday/name1.git
    sunday_install https://website.com/sunday/name1.git https://website.com/sunday/name2.git
    sunday_install --giturl https://website.com sunday/name1.git https://website.com/sunday/name2.git sunday/name3.git https://website.com/sunday/name4.git
    sunday_install /path/to/package
```
