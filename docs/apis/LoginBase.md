# LoginBase

控制会话、管理登录态，所有登录插件都应该继承自LoginBase

---

## api说明

::: sunday.utils.LoginBase
    :docstring:
    :members: checkLogin initRs

## 使用注意

1. 存在多登录态管理时需要传入唯一标识，即`ident`入参值会在生成登录关键信息文件时作为文件名尾缀，以标记下次相同ident值直接取出登录态使用;
2. initrs方法入参usehistory表示是否使用已经存在的登录态，一般建议开启，除非是登录接口需要验证登录的账密信息则需要重走登录流程;
3. initrs方法会返回session实例与是否登录的标识，当登录标识为未登录时需要重新执行登录流程.

