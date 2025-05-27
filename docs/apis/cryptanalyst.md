# 加密解密

不管是国标还是非国标，不管是对称还是非对称，直接拿来用

---

## API说明

### PYSunday内部使用的加解密

::: sunday.core.aesCbcEncrypt
    :docstring:

::: sunday.core.aesCbcDecrypt
    :docstring:

### 外部常见的加解密

#### 基于cryptoJS

::: sunday.utils.cryptByCryptoJS
    :docstring:

#### 基于JSEncrypt

::: sunday.utils.cryptByJsEncrypt
    :docstring:

#### 国家标准密码

::: sunday.utils.cryptBySm4
    :docstring:

::: sunday.utils.cryptBySm2
    :docstring:

### 可能会用到的方法

::: sunday.utils.grenKey
    :docstring:

::: sunday.utils.str2base16
    :docstring:
