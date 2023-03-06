/*
  根据密文与密钥解码出UUID值，在etax.henan.chinatax.gov.cn中提取
  示例：
  const handler = require('./aesToolsNsrd')
  console.log(handler.decryptUuid('KcOuwoUACx1ueXNAdMKAwq3Dj8OGwp7DqlHDhcKtelk9w6nCqsKsw63CiHFNwqcJWxcuwok=', 'etM8'))
*/
;(function (root, factory) {
  if (typeof exports === "object") {
    // CommonJS
    module.exports = exports = factory();
  }
  else if (typeof define === "function" && define.amd) {
    // AMD
    define([], factory);
  }
  else {
    // Global (browser)
    root.CryptoJS = factory();
  }
}(this, function () {
  var atob1 = function(r) {
    var b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var o = String(r)["replace"](/=+$/, "");
    var d = "";
    for (var c = 0, q, e, p = 0; e = o.charAt(p++); ~e && (q = c % 4 ? q * 64 + e : e,
      c++ % 4) ? d += String.fromCharCode(255 & q >> (-2 * c & 6)) : 0) {
      e = b.indexOf(e)
    }
    return d
  }

  var h = function(r, v) {
    var t = [], b = 0, q, a = "", e = "";
    r = atob1(r);
    for (var c = 0, s = r.length; c < s; c++) {
      e += "%" + ("00" + r.charCodeAt(c)["toString"](16))["slice"](-2)
    }
    r = decodeURIComponent(e);
    var u;
    for (u = 0; u < 256; u++) {
      t[u] = u
    }
    for (u = 0; u < 256; u++) {
      b = (b + t[u] + v.charCodeAt(u % v.length)) % 256;
      q = t[u];
      t[u] = t[b];
      t[b] = q
    }
    u = 0;
    b = 0;
    for (var d = 0; d < r.length; d++) {
      u = (u + 1) % 256;
      b = (b + t[u]) % 256;
      q = t[u];
      t[u] = t[b];
      t[b] = q;
      a += String.fromCharCode(r.charCodeAt(d) ^ t[(t[u] + t[b]) % 256])
    }
    return a
  };
  return {
    decryptUuid: h,
  };
}));
