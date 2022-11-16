const jsencrypt = require('./jsencrypt')

const handler = new jsencrypt.JSEncrypt

const [publicKey, ...str] = process.argv.slice(2)
handler.setPublicKey(publicKey)
const ans = str.map(each => handler.encrypt(each)).join('\n')

console.log(ans)
