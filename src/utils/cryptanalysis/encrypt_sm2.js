const sm2 = require('./sm2.js')

const [publicKey, cipherMode, ...str] = process.argv.slice(2)
const ans = str.map(each => sm2.doEncrypt(each, publicKey, Number(cipherMode))).join('\n')

console.log(ans)
