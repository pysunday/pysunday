# API-报错捕获

程序报错捕获与管理

---

## API说明

::: sunday.core.getException.getException
    :docstring:

返回CustomError对象，该对象实际化后存在code、message与allowAttr允许的属性名

NOTE: **提示**
由于CustomError对象继承自SundayError对象，因此报错捕获可直接使用SundayError对象

## 示例

### 1. 一般性使用

```python
from sunday.core.getException import getException

MyError = getException({
    10000: '错误提示1',
    10001: '错误提示2',
  })

# 样例一：
try:
    raise MyError(10000)
except MyError as err:
    print(err.code) # 10000
    print(err.message) # 错误提示1
    print(str(err)) # 10000 错误提示1

# 样例二：
try:
    raise MyError(99999, '自定义报错提示', other='其它说明')
except MyError as err:
    print(err.code) # 99999
    print(err.message) # 自定义报错提示(其它说明)
    print(str(err)) # 99999 自定义报错提示(其它说明)
```

### 2. 多个报错定义与捕获

多个CustomError实例报错可使用常规写法`except (Error1, Error2) as err`或者使用`SundayError`, 如：

```python
from sunday.core.getException import getException, SundayError

MyError1 = getException(...)
MyError2 = getException(...)
try:
    raise MyError1(...)
    raise MyError2(...)
except SundayError as err:
    ...
```

### 3. 自定义报错属性

PYSunday提供的报错对象实例化后只有`code`和`message`两个属性，在实际场景应用中，我们可能还需要标记堆栈编号、接口原始报错文本等，这个功能也是支持的，看如下示例：

```python
from sunday.core.getException import getException, SundayError

MyError = getException({ 10000: '错误提示' }, ['stackId', 'originMsg'])
try:
    raise MyError1(10000, stackId='7758258', originMsg='网站接口返回的报错json串', name='PYSunday')
except SundayError as err:
    print(err.code) # 10000
    print(err.message) # 错误提示
    print(err.stackId) # 7758258
    print(err.originMsg) # 网站接口返回的报错json串
    print(err.name) # None
    print(str(err)) # 10000 错误提示
```

WARNING: **注意**
自定义属性需要在getException方法调用的第二个入参传入，未预先指定的字段都会被抛弃，如上示例中的name，由于未在getException调用的时候定义，因此打印出来是None
