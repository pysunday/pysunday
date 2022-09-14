#!/usr/bin/env python
# coding: utf-8

import stat
import pdb
from os import path, chmod, listdir, system
from setuptools import setup
from setuptools.command.install import install

version = '0.2.8.4'

binCwd = path.join(path.dirname(path.realpath(__file__)), 'bin')
if path.exists(binCwd):
    for name in listdir(binCwd): chmod(path.join(binCwd, name), stat.S_IRWXU)

with open('./README.md', 'r') as f:
    readme = f.read()

install_requires = []
with open("requirements.txt", "r") as fp:
    for line in fp:
        line.strip()
        if line:
            install_requires.append(line.strip())

class Install(install):
    def run(self):
        install.run(self)
        system('pip3 install -r requirements.txt')
        print('''
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
''')

setup(
    name='pysunday',
    version=version,
    description='一款目标明确的敏捷开发工具',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='ct',
    author_email='it17621000@163.com',
    python_requires='>3',
    packages=['sunday', 'sunday.core', 'sunday.utils', 'sunday.login', 'sunday.tools'],
    package_dir={'sunday': 'src'},
    install_requires=install_requires,
    extras_require={
        'debug': ['ipython', 'ipdb']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
    scripts=['bin/sunday_install'],
    dependency_links=[
        'https://pypi.org/simple/'
    ],
    cmdclass={
        'install': Install,
    }
)
