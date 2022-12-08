const CryptoJS = require('./cryptojs')

const [publicKey, ...str] = process.argv.slice(2)
const key = CryptoJS.enc.Utf8.parse(publicKey);   

const ans = str.map(each => {
  const text = CryptoJS.enc.Utf8.parse(each);  
  const encrypted = CryptoJS.AES.encrypt(text, key, { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 });
  return encrypted.toString();
}).join('\n')

console.log(ans)
