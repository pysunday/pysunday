const handler = require('./aesToolsNsrd')

const [publicKey, ...str] = process.argv.slice(2)

const ans = str.map(each => handler.decryptUuid(each, publicKey)).join('\n')

console.log(ans)
