import dev from './env.dev'
import test from './env.test'
import prod from './env.prod'

// 条件导入本地开发配置 - 使用 require 来实现动态导入
let dev_local
try {
  dev_local = require('./env.local.dev').default
} catch (e) {
  dev_local = null
}

const envVersion = __wxConfig.envVersion
// develop | trial | release
// 开发 | 体验 | 正式

let config = dev

// 如果是开发环境且本地开发配置存在，则使用本地开发配置
if (envVersion === 'develop' && dev_local) {
  config = dev_local
} else if (envVersion === 'trial') {
  config = test
} else if (envVersion === 'release') {
  config = prod
}

export default config