# PYSunday 安装

详细指南

---

## 环境

PYSunday依赖[Python]和Python包管理工具[pip], 请确认您的系统是否存在Python及pip.

您可以执行如下命令检查软件版本号.

```console
$ python3 --version
Python 3.10.8
$ pip3 --version
pip 22.2.2 from /opt/homebrew/lib/python3.10/site-packages/pip (python 3.10)
```

## 安装PYSunday

<!-- termynal -->
```
$ pip3 install pysunday
---> 100%
安装完成
```

### pypi方式安装

使用pip安装`PYSunday`包, 如果您系统环境配置混乱，可在pip3前面加`python3 -m`执行安装

安装：`pip3 install pysunday`

卸载：`pip3 uninstall pysunday`

更新：`pip3 install --upgrade pysunday`

### 源代码安装

下载源代码并进入目录执行安装命令：

```bash
git clone git@github.com:pysunday/pysunday.git
cd pysunday
python3 setup.py install
```

执行安装命令后界面打印如下安装成功：

```text
                          #
  mmm   m   m  m mm    mmm#   mmm   m   m
 #   "  #   #  #"  #  #" "#  "   #  "m m"
  """m  #   #  #   #  #   #  m"""#   #m#
 "mmm"  "mm"#  #   #  "#m##  "mm"#   "#
                                     m"
                                    ""

安装成功, sunday让生活更美好!

自定义目录配置:
    export SUNDAY_ROOT=~/.sunday
    export PATH=$SUNDAY_ROOT/bin:$PATH
默认目录配置:
    export PATH=~/.sunday/bin:$PATH
```

### 安装成功后初始化

安装成功后需要执行`python3 -c '__import__("sunday.core.init")'`让sunday自动检查并初始化执行环境, 暂时只支持`zsh`、`bash`的环境初始化

或者手动修改shell的rc文件，添加：

```shell
export SUNDAY_ROOT=~/.sunday
export PATH=$SUNDAY_ROOT/bin:$PATH
```

## 检查是否安装成功

执行如下命令查看是否已经安装PYSunday及版本：

```bash
$ pip3 freeze | grep pysunday
pysunday==0.2.8.23
```

[Python]: https://www.python.org/
[pip]: https://pip.readthedocs.io/en/stable/installing/
