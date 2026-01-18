// SHA256 implementation for WeChat Mini Programs
// Simple hash function - in production, you might want to use a more robust library

// UTF-8 编码函数，用于将 Unicode 字符串转换为字节数组
function utf8Encode(str) {
  let result = '';
  for (let i = 0; i < str.length; i++) {
    const charCode = str.charCodeAt(i);
    
    if (charCode < 0x80) {
      // ASCII 字符
      result += String.fromCharCode(charCode);
    } else if (charCode < 0x800) {
      // 2 字节 UTF-8 序列
      result += String.fromCharCode(0xC0 | (charCode >> 6));
      result += String.fromCharCode(0x80 | (charCode & 0x3F));
    } else if (charCode < 0x10000) {
      // 3 字节 UTF-8 序列
      result += String.fromCharCode(0xE0 | (charCode >> 12));
      result += String.fromCharCode(0x80 | ((charCode >> 6) & 0x3F));
      result += String.fromCharCode(0x80 | (charCode & 0x3F));
    } else if (charCode < 0x110000) {
      // 4 字节 UTF-8 序列
      result += String.fromCharCode(0xF0 | (charCode >> 18));
      result += String.fromCharCode(0x80 | ((charCode >> 12) & 0x3F));
      result += String.fromCharCode(0x80 | ((charCode >> 6) & 0x3F));
      result += String.fromCharCode(0x80 | (charCode & 0x3F));
    }
  }
  return result;
}

function sha256(str) {
  // 先将输入字符串转换为 UTF-8 编码的字节数组
  const utf8String = utf8Encode(str);

  function rightRotate(value, amount) {
    return (value >>> amount) | (value << (32 - amount));
  }

  var mathPow = Math.pow;
  var maxWord = mathPow(2, 32);
  var lengthProperty = 'length';
  var i, j; // Used as a counter across the whole file
  var result = '';

  var words = [];
  var asciiBitLength = utf8String[lengthProperty] * 8;

  //* Begin initialization constants
  var h0 = 0x6A09E667;
  var h1 = 0xBB67AE85;
  var h2 = 0x3C6EF372;
  var h3 = 0xA54FF53A;
  var h4 = 0x510E527F;
  var h5 = 0x9B05688C;
  var h6 = 0x1F83D9AB;
  var h7 = 0x5BE0CD19;
  var k = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
    0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
    0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
    0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2
  ];
  var i = 0x00;
  //* End initialization constants

  // Padding
  let paddedString = utf8String + '\x80'; // Append 80 to the binary string
  while ((paddedString[lengthProperty] % 64) - 56 !== 0) {
    paddedString += '\x00'; // Pad with zeros
  }

  // Append original length as 64-bit big-endian integer
  // First append 8 zero bytes
  for (let idx = 0; idx < 8; idx++) {
    paddedString += '\x00';
  }
  
  // Then overwrite last 8 bytes with original bit length
  const bitLen = utf8String[lengthProperty] * 8;
  for (let idx = 0; idx < 8; idx++) {
    const byte = (bitLen >>> (idx * 8)) & 0xFF;
    paddedString = paddedString.substring(0, paddedString.length - 8 + idx) + String.fromCharCode(byte) + paddedString.substring(paddedString.length - 7 + idx);
  }

  // Process padded message in 512-bit chunks
  var processedBitLength = paddedString[lengthProperty] * 8;
  var chunkCount = processedBitLength / 512;

  for (var chunkIndex = 0; chunkIndex < chunkCount; chunkIndex++) {
    // Break chunk into sixteen 32-bit words w[j], 0 ≤ j ≤ 15
    var w = new Array(64);
    for (var j = 0; j < 16; j++) {
      w[j] = (
        (paddedString.charCodeAt(chunkIndex * 64 + j * 4) << 24) |
        (paddedString.charCodeAt(chunkIndex * 64 + j * 4 + 1) << 16) |
        (paddedString.charCodeAt(chunkIndex * 64 + j * 4 + 2) << 8) |
        (paddedString.charCodeAt(chunkIndex * 64 + j * 4 + 3))
      ) >>> 0; // Ensure unsigned 32-bit integer
    }

    // Extend the sixteen 32-bit words into sixty-four 32-bit words
    for (var j = 16; j < 64; j++) {
      var s0 = rightRotate(w[j-15], 7) ^ rightRotate(w[j-15], 18) ^ (w[j-15] >>> 3);
      var s1 = rightRotate(w[j-2], 17) ^ rightRotate(w[j-2], 19) ^ (w[j-2] >>> 10);
      w[j] = (w[j-16] + s0 + w[j-7] + s1) >>> 0;
    }

    // Initialize working variables to current hash value
    var a = h0;
    var b = h1;
    var c = h2;
    var d = h3;
    var e = h4;
    var f = h5;
    var g = h6;
    var h = h7;

    // Main loop
    for (var j = 0; j < 64; j++) {
      var S1 = rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25);
      var ch = (e & f) ^ (~e & g);
      var temp1 = (h + S1 + ch + k[j] + w[j]) >>> 0;
      var S0 = rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22);
      var maj = (a & b) ^ (a & c) ^ (b & c);
      var temp2 = (S0 + maj) >>> 0;

      h = g;
      g = f;
      f = e;
      e = (d + temp1) >>> 0;
      d = c;
      c = b;
      b = a;
      a = (temp1 + temp2) >>> 0;
    }

    // Add this chunk's hash to result so far
    h0 = (h0 + a) >>> 0;
    h1 = (h1 + b) >>> 0;
    h2 = (h2 + c) >>> 0;
    h3 = (h3 + d) >>> 0;
    h4 = (h4 + e) >>> 0;
    h5 = (h5 + f) >>> 0;
    h6 = (h6 + g) >>> 0;
    h7 = (h7 + h) >>> 0;
  }

  // Produce the final hash value (big-endian)
  var digest = '';
  digest += ('00000000' + h0.toString(16)).slice(-8);
  digest += ('00000000' + h1.toString(16)).slice(-8);
  digest += ('00000000' + h2.toString(16)).slice(-8);
  digest += ('00000000' + h3.toString(16)).slice(-8);
  digest += ('00000000' + h4.toString(16)).slice(-8);
  digest += ('00000000' + h5.toString(16)).slice(-8);
  digest += ('00000000' + h6.toString(16)).slice(-8);
  digest += ('00000000' + h7.toString(16)).slice(-8);

  return digest;
}

export default sha256;