# API-加密解密

不管是国标还是非国标，不管是对称还是非对称，直接拿来用

---

## API说明

### PYSunday内部使用的加解密

::: sunday.core.aesCbc.aesCbcDecrypt
    :docstring:

::: sunday.core.aesCbc.aesCbcEncrypt
    :docstring:

### 外部常见的加解密

#### 基于cryptoJS

::: sunday.utils.cryptanalyst.cryptByCryptoJS
    :docstring:

#### 基于JSEncrypt

::: sunday.utils.cryptanalyst.cryptByJsEncrypt
    :docstring:

#### 国家标准密码

::: sunday.utils.cryptanalyst.cryptBySm4
    :docstring:

::: sunday.utils.cryptanalyst.cryptBySm2
    :docstring:

### 可能会用到的方法

::: sunday.utils.cryptanalyst.grenKey
    :docstring:

::: sunday.utils.cryptanalyst.str2base16
    :docstring:
