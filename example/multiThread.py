from sunday.core.MultiThread import MultiThread
import time, random

thread_num = 9 # 线程数
datas = list(range(30))
def handler(items, idx, update):
    for item in items:
        time.sleep(random.random())
        update()
print('任务开始')
MultiThread(datas, lambda *args: [handler, args], thread_num).start(isBar=True)
print('任务结束')

