import dev from './env.dev'
import test from './env.test'
import prod from './env.prod'

const envVersion = __wxConfig.envVersion
// develop | trial | release
// 开发 | 体验 | 正式

let config = dev

if (envVersion === 'trial') {
  config = test
}

if (envVersion === 'release') {
  config = prod
}

export default config