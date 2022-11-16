# coding: utf-8
import threading

class MultiThread():
    """ 多线程
    Arguments:
      items: 配置列表
      func: 根据配置返回target及args, 可返回字典或数组, 如果是数组则第一个值为方法第二个值为入参
    Attributes:
      start: 开启多线程任务
    """
    def __init__(self, items, func):
        self.threads = []
        for idx, item in enumerate(items):
            params = func(item, idx)
            args = params if type(params) == dict else {}
            if type(params) == list:
                args['target'], args['args'] = params
            self.threads.append(threading.Thread(**args))
    
    def start(self, isDelay=True):
        for i in self.threads: i.start()
        if isDelay:
            for i in self.threads: i.join()
