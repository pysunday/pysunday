# coding: utf-8
import threading
import tqdm

class MultiThread():
    """ 多线程
    Arguments:
      items: 配置列表
      func: 根据配置返回target及args, 可返回字典或数组, 如果是数组则第一个值为方法第二个值为入参
      tnum: 线程数, 如果传入的items未按线程数分组则可传入tnum程序自动分组，如已分组该值勿传
    Attributes:
      start: 开启多线程任务
    """
    def __init__(self, items, func, tnum=None):
        if tnum: items = [[item for item in items[i::tnum]] for i in range(tnum)]
        self.threads = []
        self.data_count = 0
        self.pbar = None
        def pbar_update():
            if self.pbar:
                self.pbar.update(1)
        for idx, item in enumerate(items):
            self.data_count += len(item)
            params = func(item, idx, pbar_update)
            args = params if type(params) == dict else {}
            if type(params) == list:
                args['target'], args['args'] = params
            self.threads.append(threading.Thread(**args))
    
    def start(self, isDelay=True, isBar=False):
        """
        Arguments:
            isDelay: 是否后台执行
            isBar：是否显示进度条
        """
        for i in self.threads: i.start()
        if isDelay:
            isShowBar = isBar and self.data_count > 0
            if isShowBar:
                self.pbar = tqdm.tqdm(total=self.data_count)
            for i in self.threads: i.join()
            if isShowBar:
                self.pbar.close()
                self.pbar = None
