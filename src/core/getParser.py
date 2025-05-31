# coding: utf-8
import argparse
from pydash import pick, omit, get
from .common import pascal_to_snake
from sunday.core.logger import setLogLevel, logLevelKeys

arr = ['version', 'params']

def formatter(prog):
    return argparse.RawDescriptionHelpFormatter(prog, indent_increment=2, max_help_position=100, width=140)

def getParserDefault(config, name='DEFAULT'):
    '''用于返回命令入参的默认值对象
    Args:
        config(dict): 为命令入参
        name(str): 默认为DEAFULT, 如果返回指定子命令的默认值, 可替代为子命令名称
    Usages:
        class MyClass:
            def __init__(self, CMDINFO):
                self.__dict__.update(getParserDefault(CMDINFO))
    '''
    arr = get(config, '.'.join(['params', name])) or []
    obj = {}
    for item in arr:
        obj[item['dest']] = get(item, 'default')
    return obj

def getParser(**argvs):
    '''传入对象, 除以下参数, 其它参数用于实例化parser使用;
    Args:
        version(str): 程序版本
        params(dict): 命令入参
            params.DEFAULT(list): 默认命令入参
            params.SUBCONFIG(dict): 子命令配置
            params.name(list): 名称为name的子命令的命令入参
        description(str): 描述
        epilog(str): 说明
    Returns: parser, [subparsersObj]
        存在子命令则返回subparsersObj
    Usages:
        CMDINFO = {
            "version": '0.0.1',
            "description": "命令描述",
            "epilog": "使用样例：%(prog)s name -m 176****0163",
            'params': {
                'DEFAULT': [
                    {
                        'name': 'name',
                        'help': '不需要-前缀的入参',
                        'default': './',
                        'nargs': '?'
                    },
                    {
                        'name': ['-m', '--mobile'],
                        'help': '手机号',
                        'dest': 'mobile',
                    },
                ],
            }
        }
        parser = getParser(**CMDINFO)
        handle = parser.parse_args(namespace=MySearch())
    '''
    parserObj, commandObj = omit(argvs, arr), pick(argvs, arr)
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=formatter,
        **parserObj
    )
    parser._positionals.title = 'Positionals'
    parser._optionals.title = 'Optional'
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
                name = cfg['name'] if type(cfg['name']) == list else [cfg['name']]
                if 'metavar' not in cfg and 'dest' in cfg and get(tar, 'action') not in ['store_false', 'store_true']:
                    tar['metavar'] = pascal_to_snake(cfg['dest']).upper()
                tarparser.add_argument(*name, **tar)
    # 兼容老用法
    parser.add_argument('-v', '--version', action='version', version=commandObj['version'] or '0.0.0', help='当前程序版本')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='打印帮助说明')
    parser.add_argument(
            '--loglevel',
            default='debug',
            metavar='LEVEL',
            dest='loglevel',
            choices=[*logLevelKeys, *[key.upper() for key in logLevelKeys]],
            help=f'日志等级（{"、".join(logLevelKeys)}）, 默认debug')
    def parse_args(*args, **kwargs):
        setLogLevel(parser.parse_known_args()[0].loglevel)
        return parser.parse_known_args(*args, **kwargs)[0]
    parser.parse_args = parse_args
    if not subparsers: return parser
    return parser, subparsersObj
