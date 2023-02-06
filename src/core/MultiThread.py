# coding: utf-8
import threading
import tqdm

class MultiThread():
    """
    多线程任务调用控制

    **Usage:**

    ```
    >>> from sunday.core.MultiThread import MultiThread
    >>> handler = lambda items, threadId, barUpdate: print(item)
    >>> MultiThread([1, 2, 3, 4], lambda *args: [handler, args], 2).start()
    ```

    **Parameters:**

    * **items:** `list` -- 任务列表
    * **func:** `def` -- 根据配置返回target及args, 可返回字典或数组, 如果是数组则第一个值为方法第二个值为入参
    * **tnum:** `int` -- 线程数, 如果传入的items未按线程数分组则可传入tnum程序自动分组，如已分组该值勿传

    **Return:** `thread`
    """
    def __init__(self, items, func, tnum=None):
        if tnum: items = [[item for item in items[i::tnum]] for i in range(tnum)]
        self.threads = []
        self.data_count = 0
        self.pbar = None
        def pbar_update(step=1):
            if self.pbar:
                self.pbar.update(step)
        for idx, item in enumerate(items):
            self.data_count += len(item)
            try:
                params = func(item, idx, pbar_update)
            except Exception as e:
                params = func(item, idx)
            args = params if type(params) == dict else {}
            if type(params) == list:
                args['target'], args['args'] = params
            self.threads.append(threading.Thread(**args))
    
    def start(self, isDelay=True, isBar=False):
        """
        开始执行多线程任务

        **Parameters:**

        * **isDelay:** `bool` -- 是否等待执行完成，默认为True，False表示后台运行
        * **isBar:** `bool` -- 是否显示进度条, 默认False
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
