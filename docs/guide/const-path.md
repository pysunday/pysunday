# PYSunday的全局常量与路径

全局常量与路径

---

## 全局常量

PYSunday代码运行即会写入内存的常量，贯穿整个代码运行，因此在任何时候都可以拿到常量值使用，一般插件开发不需要用到

获取和设置常量值的方法在`sunday.core.globalvar`中的`getvar`与`setvar`方法

常量键名以`sdvar_`开头

### 1. sdvar_logger

获取名称为SUNDAY的日志实例对象，用于PYSunday内部日志打印使用，使用方式：

```
>>> from sunday.core import getvar, sdvar_logger
>>> getvar(sdvar_logger).debug('日志打印')
[20:24:06.470] DEBUG  : <SUNDAY> 日志打印
```

### 2. sdvar_loggerid

日志缓存文件的文件名

### 3. sdvar_premust

返回布尔值，用于标记全局常量是否已经创建过

### 4. sdvar_exectime

获取程序运行时间及两次调用间隔的代码执行时间，返回两个元素组成的元祖，第一个元素为距离上次执行方法的时间间隔，第二个元素为程序总的运行时间，使用方式：

```
>>> from sunday.core import getvar, sdvar_exectime
>>> getvar(sdvar_exectime)()
(2.0566060543060303, 2.0566060543060303)
>>> getvar(sdvar_exectime)()
(2.3964710235595703, 4.453077077865601)
```

### 5. sdvar_exception

获取PYSunday内部使用的报错类，可以用基类`SundayError`进行捕获，使用方式：

```
>>> from sunday.core import getvar, sdvar_exception
>>> raise getvar(sdvar_exception)(10000, '错误提示')
CustomError: '10000 错误'
```

### 6. sdvar_loglevel

获取当前PYSunday日志打印等级，默认为`ERROR`，可通过修改`$PYSUNDAY/config.ini`中的`[LOGGING][level]`初始化定义，或者运行`sunday.core.logger.setLogLevel`方法修改，如：

```
>>> from sunday.core import getvar, sdvar_loglevel, setLogLevel
>>> getvar(sdvar_loglevel)
ERROR
>>> setLogLevel('DEBUG')
>>> getvar(sdvar_loglevel)
DEBUG
```

## 程序运行路径

想获取PYSunday的运行目录、日志目录、插件目录等就可以通过程序运行路径文件中拿到。

引入路径模块：`from sunday.core import paths`或`import sunday.core.paths as paths`

名称 | 路径 | 说明
---- | ---- | ----
`paths.rootCwd` | `$SUNDAY_ROOT` | 程序家目录
`paths.logCwd` | `$SUNDAY_ROOT/log` | 日志文件存储目录
`paths.binCwd` | `$SUNDAY_ROOT/bin` | PYSunday命令运行目录
`paths.moduleLockCwd` | `$SUNDAY_ROOT/module-lock.json` | 插件信息锁文件路径
`paths.sundayLoginCwd` | `path/to/site-packages/sunday/login` | 登录插件代码目录
`paths.sundayToolsCwd` | `path/to/site-packages/sunday/tools` | 工具插件代码目录


