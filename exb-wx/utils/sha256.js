/**
 * SHA-256 (UTF-8)
 * Compatible with WeChat Mini Program
 */

function sha256(ascii) {
  // UTF-8 encode
  ascii = utf8Encode(ascii)

  const mathPow = Math.pow
  const maxWord = mathPow(2, 32)
  let result = ''

  const words = []
  const asciiBitLength = ascii.length * 8

  const hash = []
  const k = []
  let primeCounter = 0

  // 初始化 hash 和 k
  const isPrime = num => {
    for (let i = 2, sqrt = Math.sqrt(num); i <= sqrt; i++) {
      if (num % i === 0) return false
    }
    return true
  }

  const frac = num => ((num - Math.floor(num)) * maxWord) | 0

  for (let candidate = 2; primeCounter < 64; candidate++) {
    if (isPrime(candidate)) {
      if (primeCounter < 8) {
        hash[primeCounter] = frac(Math.pow(candidate, 1 / 2))
      }
      k[primeCounter] = frac(Math.pow(candidate, 1 / 3))
      primeCounter++
    }
  }

  // 填充
  ascii += '\x80'
  while ((ascii.length % 64) !== 56) ascii += '\x00'

  for (let i = 0; i < ascii.length; i++) {
    const j = ascii.charCodeAt(i)
    words[i >> 2] |= j << ((3 - i) % 4) * 8
  }

  words.push((asciiBitLength / maxWord) | 0)
  words.push(asciiBitLength)

  // 计算
  for (let j = 0; j < words.length;) {
    const w = words.slice(j, j += 16)
    const oldHash = hash.slice(0)

    for (let i = 0; i < 64; i++) {
      const w15 = w[i - 15], w2 = w[i - 2]

      const a = hash[0], e = hash[4]
      const temp1 = hash[7]
        + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25))
        + ((e & hash[5]) ^ (~e & hash[6]))
        + k[i]
        + (w[i] = i < 16 ? w[i] : (
          w[i - 16]
          + (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3))
          + w[i - 7]
          + (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))
        ) | 0)

      const temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22))
        + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]))

      hash.unshift((temp1 + temp2) | 0)
      hash[4] = (hash[4] + temp1) | 0
      hash.pop()
    }

    for (let i = 0; i < 8; i++) {
      hash[i] = (hash[i] + oldHash[i]) | 0
    }
  }

  // 输出 hex
  for (let i = 0; i < 8; i++) {
    for (let j = 3; j + 1; j--) {
      const b = (hash[i] >> (j * 8)) & 255
      result += (b < 16 ? '0' : '') + b.toString(16)
    }
  }

  return result
}

// UTF-8 编码（关键：支持中文）
function utf8Encode(str) {
  return unescape(encodeURIComponent(str))
}

function rightRotate(value, amount) {
  return (value >>> amount) | (value << (32 - amount))
}

export default sha256