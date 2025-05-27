# Auth

用户输入内容的交互

---

## API说明

::: sunday.core.Auth
    :docstring:
    :members: addParams getParams

如果传入的tip或者key属于以下内容，则显示对于提示：

'USER', 'user', 'username', 'USERNAME', 'name', 'NAME' => '请输入用户名'

'PWD', 'pwd', 'PASSWORD', 'password' => '请输入密码'

'CODE', 'code' => '请输入验证码'
