const CryptoJS = require('./cryptojs')

const [publicKey, ...str] = process.argv.slice(2)
const key = CryptoJS.enc.Utf8.parse(publicKey);   

const ans = str.map(each => {
  const decrypted = CryptoJS.AES.decrypt(each, key, { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 });
  return CryptoJS.enc.Utf8.stringify(decrypted).toString()
}).join('\n')

console.log(ans)
