# cache_name

缓存实例化结果，避免重复实例化

---

## API说明

::: sunday.core.cache_name
    :docstring:

当开发单用户交互的工具命令时，可以使用cache_name包裹登录类，之后在调用登录类实例化的时候就不会重复实例化和验证登录态是否过期

**注意：该方法不适用于多用户登录的场景**

```python
@cache_name('name')
class Login(LoginBase):
    pass
```


