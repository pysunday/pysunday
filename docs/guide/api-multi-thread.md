# API-多线程

多线程控制程序高效运行

---

## API说明

::: sunday.core.MultiThread.MultiThread
    :docstring:
    :members: start

根据实例化数据情况可以分为两种实例化方式

### 1. 数据划分后传入

如数据：

```python
datas = [
  [1, 2, 3],
  [4, 5, 6]
]
```

此时两个线程分别处理 `[1, 2, 3]` 和 `[4, 5, 6]`

调用MultiThread实例化方法时, 第三个入参不用传，如：

```python
MultiThread(datas, lambda *args: [handlerFunc, args])
```

### 2. 数据传入后程序自动划分

如数据：

```python
datas = [1, 2, 3, 4, 5, 6]
```

此时两个线程分别处理 `[1, 3, 5]` 和 `[2, 4, 6]`

调用MultiThread实例化方法时, 第三个入参传入线程数量, 如：

```python
MultiThread(datas, lambda *args: [handlerFunc, args], 2)
```

WARNING: **注意**
需要注意第二个入参为回调函数，回调函数入参分别为当前进程的任务数组、当前任务编号、更新进度条的回调方法，返回参数为两个元素的数组或元祖，第一个参数为任务执行方法，第二个参数是任务执行方法的入参，形式如：`lambda *args: [handlerFunc, args]`.  
使用时注意：  
1. 传入任务方法额外入参需分解第二个参数如上面的`args`类似：`lambda *args: [handlerFunc, (*args, 'hello')]`  
2. 由于任务方法可能为多线程调用，也可能为单线程调用，因此任务方法除了数据参数其它参数建议给默认值, 如：`def handlerFunc(items, thread_id=None, barUpdate=None)`  
3. 第三个参数是进度条更新的回调，考虑单线程调用任务方法，因此建议安全调用：`barUpdate and barUpdate()`

### 执行任务

MultiThread类实例化后返回类实例需要手动执行start方法才可以开始任务

#### 是否等待执行结束

isDelay控制是否需要等待执行结束，默认为True

1. `True`: 需要等待执行结束才能执行接下来的程序代码, 如：`start(isDelay=True)`
2. `False`: 线程任务后台运行，直接开始执行接下来的程序代码, 如：`start(isDelay=False)`

#### 是否显示进度条

开启进度条显示就可以看到线程任务执行了多少, 默认不开启需要手动开启，如：`start(isBar=True)`

NOTE: **提示**
只有开启进度条显示任务方法中的barUpdate方法才能执行，barUpdate回调默认表示1个任务执行完成

## 示例

```python
from sunday.core.MultiThread import MultiThread
import time, random

thread_num = 9 # 线程数
datas = list(range(30)) # 数据
def handlerFun(items, idx=None, update=None):
    for item in items:
        # 循环处理该线程要处理的数据任务
        time.sleep(random.random()) # 等待等待时间
        update and update() # 刷新进度条
print('任务开始')
MultiThread(datas, lambda *args: [handlerFun, args], thread_num).start(isBar=True)
print('任务结束')
```

