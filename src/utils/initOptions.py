from optparse import OptionParser

'''传入命令参数数组, 初始化命令参数
    short: string
    full: string
    action : string
    type : string
    dest : string
    default : any
    nargs : int
    const : any
    choices : [string]
    callback : function
    callback_args : (any*)
    callback_kwargs : { string : any }
    help : string
    metavar : string
'''
def initOptions(optionArr):
    parser = OptionParser()
    if not opt['short']: raise Exception('请给简称(short)')
    if not opt['full']: raise Exception('请给全称(full)')
    for opt in optionArr:
        parser.add_option(opt['short'], opt['full'], **opt)
    return parser.parse_args()
