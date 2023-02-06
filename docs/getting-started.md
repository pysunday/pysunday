# 开始使用PYSunday

这个教程只做简单介绍!

---

## 安装

允许下面命令安装

```bash
python3 -m pip install pysunday
或
pip3 install pysunday
```

更多请查看 [安装教程].

## 创建一个插件(待实现)

新建一个插件是非常简单的，允许以下命令创建一个新的插件:

```bash
mkdocs new my-project
cd my-project
```

执行成功后会生成以下文件：

```console
.
├── README.md
├── __init__.py
├── main.py
├── package.json
└── params.py
```

这里的文件都是必须的，`main.py`为插件代码文件，`package.json`记录了文件的关键信息，`params.py`用于配置插件的命令参数。

## 安装插件

现在我们可以安装该插件:

```bash
sunday_install .
```

根据`package.json`文件中的配置，bin放置可执行文件的文件名，type标记是工具类插件还是登录类插件。
安装完成后，全局命令中会增加一个main命令（在bin字段中配置）。

执行如下命令查看新安装插件提供的main命令使用方式:

```bash
main -h
```

## sunday_install

sunday_install命令用于安装sunday插件，可查看该命令使用：

```bash
sunday_install -h
```

## 更多教程说明

点击 [教程] 查看PYSunday的更多特性。

想要获取pysunday的更多帮助, 请使用 [GitHub issues] 提问.

[安装教程]: guide/install.md
[GitHub discussions]: https://github.com/pysunday/pysunday/discussions
[GitHub issues]: https://github.com/pysunday/pysunday/issues
[教程]: guide/README.md

