const sm4 = require('./sm4.js')

const [publicKey, ...str] = process.argv.slice(2)
const ans = str.map(each => sm4.decrypt(each, publicKey)).join('\n')

console.log(ans)
