# 自动生成readme文档

自动生成插件的readme文档（暂时只支持命令行工具插件）

---
当开发了PySunday插件后，写readme文档挺麻烦的，可以通过该命令自动生成readme文件，之后再通过修改readme文件达到预期的内容结果。

```bash
❯ sunday_mkreadme -h
usage: sunday_mkreadme [-v] [-h] [--loglevel LEVEL] [pluginPath]

生成插件readme文件，插件路径不传时默认当前目录

Positionals:
  pluginPath        项目目录

Optional:
  -v, --version     当前程序版本
  -h, --help        打印帮助说明
  --loglevel LEVEL  日志等级（debug、info、warning、error、critical）, 默认debug

使用案例:
    sunday_mkreadme /path/to/project
```
