# coding: utf-8
import argparse
from pydash import pick, omit, get
from .common import pascal_to_snake

arr = ['version', 'params']

def formatter(prog):
    return argparse.RawDescriptionHelpFormatter(prog, indent_increment=2, max_help_position=100, width=140)

def getParserDefault(config, name='DEFAULT'):
    '''
    用于返回命令入参的默认值对象
        config<dict>: 为命令入参
        name<str>: 默认为DEAFULT, 如果返回指定子命令的默认值, 可替代为子命令名称
    '''
    arr = get(config, '.'.join(['params', name])) or []
    obj = {}
    for item in arr:
        obj[item['dest']] = get(item, 'default')
    return obj

def getParser(**argvs):
    '''
    传入对象, 除以下参数, 其它参数用于实例化parser使用;
        1. version<str>: 程序版本
        2. params<dict>: 命令入参
            params.DEFAULT<list>: 默认命令入参
            params.SUBCONFIG<dict>: 子命令配置
            params[name]<list>: 名称为name的子命令的命令入参
        实例化用如: description、epilog等, 具体可参考argparse模块
    '''
    parserObj, commandObj = omit(argvs, arr), pick(argvs, arr)
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=formatter,
        **parserObj
    )
    parser._positionals.title = 'Positionals'
    parser._optionals.title = 'Optional'
    parser.add_argument('-v', '--version', action='version', version=commandObj['version'] or '0.0.0', help='当前程序版本')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='打印帮助说明')
    subparsers = None
    subparsersObj = {}
    if 'params' in commandObj and type(commandObj['params']) == dict:
        paramsCfg = commandObj['params']
        if 'SUBCONFIG' in paramsCfg and type(paramsCfg['SUBCONFIG']) == dict:
            subparsers = parser.add_subparsers(**paramsCfg['SUBCONFIG'])
        for (name, cfgs) in list(commandObj['params'].items()):
            tarparser = None
            if name == 'SUBCONFIG' or type(cfgs) != list:
                continue
            elif name == 'DEFAULT':
                tarparser = parser
            elif subparsers:
                tarparser = subparsers.add_parser(name)
                subparsersObj[name] = tarparser
            else:
                continue
            for cfg in cfgs:
                tar = omit(cfg, ['name'])
                if 'metavar' not in cfg and 'dest' in cfg and get(tar, 'action') not in ['store_false', 'store_true']:
                    tar['metavar'] = pascal_to_snake(cfg['dest']).upper()
                tarparser.add_argument(*cfg['name'], **tar)
    # 兼容老用法
    if not subparsers: return parser
    return parser, subparsersObj
