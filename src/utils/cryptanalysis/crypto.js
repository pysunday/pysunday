var base64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

// Global Crypto object
var Crypto = exports.Crypto = {};

// Crypto utilities
var util = Crypto.util = {

  // Bit-wise rotate left
	rotl: function (n, b) {
		return (n << b) | (n >>> (32 - b));
	},

	// Bit-wise rotate right
	rotr: function (n, b) {
		return (n << (32 - b)) | (n >>> b);
	},

	// Swap big-endian to little-endian and vice versa
	endian: function (n) {

		// If number given, swap endian
		if (n.constructor == Number) {
			return util.rotl(n,  8) & 0x00FF00FF |
			       util.rotl(n, 24) & 0xFF00FF00;
		}

		// Else, assume array and swap all items
		for (var i = 0; i < n.length; i++)
			n[i] = util.endian(n[i]);
		return n;

	},

	// Generate an array of any length of random bytes
	randomBytes: function (n) {
		for (var bytes = []; n > 0; n--)
			bytes.push(Math.floor(Math.random() * 256));
		return bytes;
	},

	// Convert a byte array to big-endian 32-bit words
	bytesToWords: function (bytes) {
		for (var words = [], i = 0, b = 0; i < bytes.length; i++, b += 8)
			words[b >>> 5] |= bytes[i] << (24 - b % 32);
		return words;
	},

	// Convert big-endian 32-bit words to a byte array
	wordsToBytes: function (words) {
		for (var bytes = [], b = 0; b < words.length * 32; b += 8)
			bytes.push((words[b >>> 5] >>> (24 - b % 32)) & 0xFF);
		return bytes;
	},

	// Convert a byte array to a hex string
	bytesToHex: function (bytes) {
		for (var hex = [], i = 0; i < bytes.length; i++) {
			hex.push((bytes[i] >>> 4).toString(16));
			hex.push((bytes[i] & 0xF).toString(16));
		}
		return hex.join("");
	},

	// Convert a hex string to a byte array
	hexToBytes: function (hex) {
		for (var bytes = [], c = 0; c < hex.length; c += 2)
			bytes.push(parseInt(hex.substr(c, 2), 16));
		return bytes;
	},

	// Convert a string to a base-64 string
	stringToBase64: function (str, encoding) {
		var bytes;
		if ( typeof encoding != 'string') {
			bytes = UTF8.stringToBytes(str);
		} else if ( encoding.toLowerCase() == 'binary' ) {
			bytes = Binary.stringToBytes(str);
		} else if ( encoding.toLowerCase() == 'utf8' || encoding.toLowerCase() == 'utf-8' ) {
			bytes = UTF8.stringToBytes(str);
		} else {
			bytes = UTF8.stringToBytes(str);
		}

		return this.bytesToBase64(bytes);
	},

	// Convert a base-64 string to origin string
	base64ToString: function (base64, encoding) {
		var bytes, str;

		bytes = this.base64ToBytes(base64);

		if ( typeof encoding != 'string') {
			str = UTF8.bytesToString(bytes);
		} else if ( encoding.toLowerCase() == 'binary' ) {
			str = Binary.bytesToString(bytes);
		} else if ( encoding.toLowerCase() == 'utf8' || encoding.toLowerCase() == 'utf-8' ) {
			str = UTF8.bytesToString(bytes);
		} else {
			str = UTF8.bytesToString(bytes);
		}

		return str;
	},

	// Convert a byte array to a base-64 string
	bytesToBase64: function (bytes) {

		// Use browser-native function if it exists
		if (typeof btoa == "function") return btoa(Binary.bytesToString(bytes));

		for(var base64 = [], i = 0; i < bytes.length; i += 3) {
			var triplet = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2];
			for (var j = 0; j < 4; j++) {
				if (i * 8 + j * 6 <= bytes.length * 8)
					base64.push(base64map.charAt((triplet >>> 6 * (3 - j)) & 0x3F));
				else base64.push("=");
			}
		}

		return base64.join("");

	},

	// Convert a base-64 string to a byte array
	base64ToBytes: function (base64) {

		// Use browser-native function if it exists
		if (typeof atob == "function") return Binary.stringToBytes(atob(base64));

		// Remove non-base-64 characters
		base64 = base64.replace(/[^A-Z0-9+\/]/ig, "");

		for (var bytes = [], i = 0, imod4 = 0; i < base64.length; imod4 = ++i % 4) {
			if (imod4 == 0) continue;
			bytes.push(((base64map.indexOf(base64.charAt(i - 1)) & (Math.pow(2, -2 * imod4 + 8) - 1)) << (imod4 * 2)) |
			           (base64map.indexOf(base64.charAt(i)) >>> (6 - imod4 * 2)));
		}

		return bytes;

	}

};

// Crypto character encodings
var charenc = Crypto.charenc = {};

// UTF-8 encoding
var UTF8 = charenc.UTF8 = {

	// Convert a string to a byte array
	stringToBytes: function (str) {
		return Binary.stringToBytes(unescape(encodeURIComponent(str)));
	},

	// Convert a byte array to a string
	bytesToString: function (bytes) {
		return decodeURIComponent(escape(Binary.bytesToString(bytes)));
	}

};

// Binary encoding
var Binary = charenc.Binary = {

	// Convert a string to a byte array
	stringToBytes: function (str) {
		for (var bytes = [], i = 0; i < str.length; i++)
			bytes.push(str.charCodeAt(i) & 0xFF);
		return bytes;
	},

	// Convert a byte array to a string
	bytesToString: function (bytes) {
		for (var str = [], i = 0; i < bytes.length; i++)
			str.push(String.fromCharCode(bytes[i]));
		return str.join("");
	}

};
// Shortcut
var util = Crypto.util;

// Convert n to unsigned 32-bit integer
util.u32 = function (n) {
	return n >>> 0;
};

// Unsigned 32-bit addition
util.add = function () {
	var result = this.u32(arguments[0]);
	for (var i = 1; i < arguments.length; i++)
		result = this.u32(result + this.u32(arguments[i]));
	return result;
};

// Unsigned 32-bit multiplication
util.mult = function (m, n) {
	return this.add((n & 0xFFFF0000) * m,
			(n & 0x0000FFFF) * m);
};

// Unsigned 32-bit greater than (>) comparison
util.gt = function (m, n) {
	return this.u32(m) > this.u32(n);
};

// Unsigned 32-bit less than (<) comparison
util.lt = function (m, n) {
	return this.u32(m) < this.u32(n);
};

// Create pad namespace
var C_pad = Crypto.pad = {};

// Calculate the number of padding bytes required.
function _requiredPadding(cipher, message) {
    var blockSizeInBytes = cipher._blocksize * 4;
    var reqd = blockSizeInBytes - message.length % blockSizeInBytes;
    return reqd;
};

// Remove padding when the final byte gives the number of padding bytes.
var _unpadLength = function (message) {
        var pad = message.pop();
        for (var i = 1; i < pad; i++) {
            message.pop();
        }
    };

// No-operation padding, used for stream ciphers
C_pad.NoPadding = {
        pad : function (cipher,message) {},
        unpad : function (message) {}
    };

// Zero Padding.
//
// If the message is not an exact number of blocks, the final block is
// completed with 0x00 bytes. There is no unpadding.
C_pad.ZeroPadding = {
    pad : function (cipher, message) {
        var blockSizeInBytes = cipher._blocksize * 4;
        var reqd = message.length % blockSizeInBytes;
        if( reqd!=0 ) {
            for(reqd = blockSizeInBytes - reqd; reqd>0; reqd--) {
                message.push(0x00);
            }
        }
    },

    unpad : function (message) {}
};

// ISO/IEC 7816-4 padding.
//
// Pads the plain text with an 0x80 byte followed by as many 0x00
// bytes are required to complete the block.
C_pad.iso7816 = {
    pad : function (cipher, message) {
        var reqd = _requiredPadding(cipher, message);
        message.push(0x80);
        for (; reqd > 1; reqd--) {
            message.push(0x00);
        }
    },

    unpad : function (message) {
        while (message.pop() != 0x80) {}
    }
};

// ANSI X.923 padding
//
// The final block is padded with zeros except for the last byte of the
// last block which contains the number of padding bytes.
C_pad.ansix923 = {
    pad : function (cipher, message) {
        var reqd = _requiredPadding(cipher, message);
        for (var i = 1; i < reqd; i++) {
            message.push(0x00);
        }
        message.push(reqd);
    },

    unpad : _unpadLength
};

// ISO 10126
//
// The final block is padded with random bytes except for the last
// byte of the last block which contains the number of padding bytes.
C_pad.iso10126 = {
    pad : function (cipher, message) {
        var reqd = _requiredPadding(cipher, message);
        for (var i = 1; i < reqd; i++) {
            message.push(Math.floor(Math.random() * 256));
        }
        message.push(reqd);
    },

    unpad : _unpadLength
};

// PKCS7 padding
//
// PKCS7 is described in RFC 5652. Padding is in whole bytes. The
// value of each added byte is the number of bytes that are added,
// i.e. N bytes, each of value N are added.
C_pad.pkcs7 = {
    pad : function (cipher, message) {
        var reqd = _requiredPadding(cipher, message);
        for (var i = 0; i < reqd; i++) {
            message.push(reqd);
        }
    },

    unpad : _unpadLength
};

// Create mode namespace
var C_mode = Crypto.mode = {};

/**
 * Mode base "class".
 */
var Mode = C_mode.Mode = function (padding) {
    if (padding) {
        this._padding = padding;
    }
};

Mode.prototype = {
    encrypt: function (cipher, m, iv) {
        this._padding.pad(cipher, m);
        this._doEncrypt(cipher, m, iv);
    },

    decrypt: function (cipher, m, iv) {
        this._doDecrypt(cipher, m, iv);
        this._padding.unpad(m);
    },

    // Default padding
    _padding: C_pad.iso7816
};


/**
 * Electronic Code Book mode.
 * 
 * ECB applies the cipher directly against each block of the input.
 * 
 * ECB does not require an initialization vector.
 */
var ECB = C_mode.ECB = function () {
    // Call parent constructor
    Mode.apply(this, arguments);
};

// Inherit from Mode
var ECB_prototype = ECB.prototype = new Mode;

// Concrete steps for Mode template
ECB_prototype._doEncrypt = function (cipher, m, iv) {
    var blockSizeInBytes = cipher._blocksize * 4;
    // Encrypt each block
    for (var offset = 0; offset < m.length; offset += blockSizeInBytes) {
        cipher._encryptblock(m, offset);
    }
};
ECB_prototype._doDecrypt = function (cipher, c, iv) {
    var blockSizeInBytes = cipher._blocksize * 4;
    // Decrypt each block
    for (var offset = 0; offset < c.length; offset += blockSizeInBytes) {
        cipher._decryptblock(c, offset);
    }
};

// ECB never uses an IV
ECB_prototype.fixOptions = function (options) {
    options.iv = [];
};


/**
 * Cipher block chaining
 * 
 * The first block is XORed with the IV. Subsequent blocks are XOR with the
 * previous cipher output.
 */
var CBC = C_mode.CBC = function () {
    // Call parent constructor
    Mode.apply(this, arguments);
};

// Inherit from Mode
var CBC_prototype = CBC.prototype = new Mode;

// Concrete steps for Mode template
CBC_prototype._doEncrypt = function (cipher, m, iv) {
    var blockSizeInBytes = cipher._blocksize * 4;

    // Encrypt each block
    for (var offset = 0; offset < m.length; offset += blockSizeInBytes) {
        if (offset == 0) {
            // XOR first block using IV
            for (var i = 0; i < blockSizeInBytes; i++)
            m[i] ^= iv[i];
        } else {
            // XOR this block using previous crypted block
            for (var i = 0; i < blockSizeInBytes; i++)
            m[offset + i] ^= m[offset + i - blockSizeInBytes];
        }
        // Encrypt block
        cipher._encryptblock(m, offset);
    }
};
CBC_prototype._doDecrypt = function (cipher, c, iv) {
    var blockSizeInBytes = cipher._blocksize * 4;

    // At the start, the previously crypted block is the IV
    var prevCryptedBlock = iv;

    // Decrypt each block
    for (var offset = 0; offset < c.length; offset += blockSizeInBytes) {
        // Save this crypted block
        var thisCryptedBlock = c.slice(offset, offset + blockSizeInBytes);
        // Decrypt block
        cipher._decryptblock(c, offset);
        // XOR decrypted block using previous crypted block
        for (var i = 0; i < blockSizeInBytes; i++) {
            c[offset + i] ^= prevCryptedBlock[i];
        }
        prevCryptedBlock = thisCryptedBlock;
    }
};


/**
 * Cipher feed back
 * 
 * The cipher output is XORed with the plain text to produce the cipher output,
 * which is then fed back into the cipher to produce a bit pattern to XOR the
 * next block with.
 * 
 * This is a stream cipher mode and does not require padding.
 */
var CFB = C_mode.CFB = function () {
    // Call parent constructor
    Mode.apply(this, arguments);
};

// Inherit from Mode
var CFB_prototype = CFB.prototype = new Mode;

// Override padding
CFB_prototype._padding = C_pad.NoPadding;

// Concrete steps for Mode template
CFB_prototype._doEncrypt = function (cipher, m, iv) {
    var blockSizeInBytes = cipher._blocksize * 4,
        keystream = iv.slice(0);

    // Encrypt each byte
    for (var i = 0; i < m.length; i++) {

        var j = i % blockSizeInBytes;
        if (j == 0) cipher._encryptblock(keystream, 0);

        m[i] ^= keystream[j];
        keystream[j] = m[i];
    }
};
CFB_prototype._doDecrypt = function (cipher, c, iv) {
    var blockSizeInBytes = cipher._blocksize * 4,
        keystream = iv.slice(0);

    // Encrypt each byte
    for (var i = 0; i < c.length; i++) {

        var j = i % blockSizeInBytes;
        if (j == 0) cipher._encryptblock(keystream, 0);

        var b = c[i];
        c[i] ^= keystream[j];
        keystream[j] = b;
    }
};


/**
 * Output feed back
 * 
 * The cipher repeatedly encrypts its own output. The output is XORed with the
 * plain text to produce the cipher text.
 * 
 * This is a stream cipher mode and does not require padding.
 */
var OFB = C_mode.OFB = function () {
    // Call parent constructor
    Mode.apply(this, arguments);
};

// Inherit from Mode
var OFB_prototype = OFB.prototype = new Mode;

// Override padding
OFB_prototype._padding = C_pad.NoPadding;

// Concrete steps for Mode template
OFB_prototype._doEncrypt = function (cipher, m, iv) {

    var blockSizeInBytes = cipher._blocksize * 4,
        keystream = iv.slice(0);

    // Encrypt each byte
    for (var i = 0; i < m.length; i++) {

        // Generate keystream
        if (i % blockSizeInBytes == 0)
            cipher._encryptblock(keystream, 0);

        // Encrypt byte
        m[i] ^= keystream[i % blockSizeInBytes];

    }
};
OFB_prototype._doDecrypt = OFB_prototype._doEncrypt;

/**
 * Counter
 * @author Gergely Risko
 *
 * After every block the last 4 bytes of the IV is increased by one
 * with carry and that IV is used for the next block.
 *
 * This is a stream cipher mode and does not require padding.
 */
var CTR = C_mode.CTR = function () {
    // Call parent constructor
    Mode.apply(this, arguments);
};

// Inherit from Mode
var CTR_prototype = CTR.prototype = new Mode;

// Override padding
CTR_prototype._padding = C_pad.NoPadding;

CTR_prototype._doEncrypt = function (cipher, m, iv) {
    var blockSizeInBytes = cipher._blocksize * 4;

    for (var i = 0; i < m.length;) {
        // do not lose iv
        var keystream = iv.slice(0);

        // Generate keystream for next block
        cipher._encryptblock(keystream, 0);

        // XOR keystream with block
        for (var j = 0; i < m.length && j < blockSizeInBytes; j++, i++) {
            m[i] ^= keystream[j];
        }

        // Increase IV
        if(++(iv[blockSizeInBytes-1]) == 256) {
            iv[blockSizeInBytes-1] = 0;
            if(++(iv[blockSizeInBytes-2]) == 256) {
                iv[blockSizeInBytes-2] = 0;
                if(++(iv[blockSizeInBytes-3]) == 256) {
                    iv[blockSizeInBytes-3] = 0;
                    ++(iv[blockSizeInBytes-4]);
                }
            }
        }
    }
};
CTR_prototype._doDecrypt = CTR_prototype._doEncrypt;


exports.encrypt = (function() {
      var r, o, a, i, u;
      r = util,
      o = UTF8,
      a = function(e) {
          return null != e && (n(e) || function(e) {
              return "function" == typeof e.readFloatLE && "function" == typeof e.slice && n(e.slice(0, 0))
          }(e) || !!e._isBuffer)
      },
      i = Binary,
      (u = function(e, t) {
          e.constructor == String ? e = t && "binary" === t.encoding ? i.stringToBytes(e) : o.stringToBytes(e) : a(e) ? e = Array.prototype.slice.call(e, 0) : Array.isArray(e) || e.constructor === Uint8Array || (e = e.toString());
          for (var n = r.bytesToWords(e), l = 8 * e.length, c = 1732584193, s = -271733879, f = -1732584194, p = 271733878, d = 0; d < n.length; d++)
              n[d] = 16711935 & (n[d] << 8 | n[d] >>> 24) | 4278255360 & (n[d] << 24 | n[d] >>> 8);
          n[l >>> 5] |= 128 << l % 32,
          n[14 + (l + 64 >>> 9 << 4)] = l;
          var h = u._ff
            , y = u._gg
            , v = u._hh
            , m = u._ii;
          for (d = 0; d < n.length; d += 16) {
              var g = c
                , b = s
                , O = f
                , w = p;
              c = h(c, s, f, p, n[d + 0], 7, -680876936),
              p = h(p, c, s, f, n[d + 1], 12, -389564586),
              f = h(f, p, c, s, n[d + 2], 17, 606105819),
              s = h(s, f, p, c, n[d + 3], 22, -1044525330),
              c = h(c, s, f, p, n[d + 4], 7, -176418897),
              p = h(p, c, s, f, n[d + 5], 12, 1200080426),
              f = h(f, p, c, s, n[d + 6], 17, -1473231341),
              s = h(s, f, p, c, n[d + 7], 22, -45705983),
              c = h(c, s, f, p, n[d + 8], 7, 1770035416),
              p = h(p, c, s, f, n[d + 9], 12, -1958414417),
              f = h(f, p, c, s, n[d + 10], 17, -42063),
              s = h(s, f, p, c, n[d + 11], 22, -1990404162),
              c = h(c, s, f, p, n[d + 12], 7, 1804603682),
              p = h(p, c, s, f, n[d + 13], 12, -40341101),
              f = h(f, p, c, s, n[d + 14], 17, -1502002290),
              c = y(c, s = h(s, f, p, c, n[d + 15], 22, 1236535329), f, p, n[d + 1], 5, -165796510),
              p = y(p, c, s, f, n[d + 6], 9, -1069501632),
              f = y(f, p, c, s, n[d + 11], 14, 643717713),
              s = y(s, f, p, c, n[d + 0], 20, -373897302),
              c = y(c, s, f, p, n[d + 5], 5, -701558691),
              p = y(p, c, s, f, n[d + 10], 9, 38016083),
              f = y(f, p, c, s, n[d + 15], 14, -660478335),
              s = y(s, f, p, c, n[d + 4], 20, -405537848),
              c = y(c, s, f, p, n[d + 9], 5, 568446438),
              p = y(p, c, s, f, n[d + 14], 9, -1019803690),
              f = y(f, p, c, s, n[d + 3], 14, -187363961),
              s = y(s, f, p, c, n[d + 8], 20, 1163531501),
              c = y(c, s, f, p, n[d + 13], 5, -1444681467),
              p = y(p, c, s, f, n[d + 2], 9, -51403784),
              f = y(f, p, c, s, n[d + 7], 14, 1735328473),
              c = v(c, s = y(s, f, p, c, n[d + 12], 20, -1926607734), f, p, n[d + 5], 4, -378558),
              p = v(p, c, s, f, n[d + 8], 11, -2022574463),
              f = v(f, p, c, s, n[d + 11], 16, 1839030562),
              s = v(s, f, p, c, n[d + 14], 23, -35309556),
              c = v(c, s, f, p, n[d + 1], 4, -1530992060),
              p = v(p, c, s, f, n[d + 4], 11, 1272893353),
              f = v(f, p, c, s, n[d + 7], 16, -155497632),
              s = v(s, f, p, c, n[d + 10], 23, -1094730640),
              c = v(c, s, f, p, n[d + 13], 4, 681279174),
              p = v(p, c, s, f, n[d + 0], 11, -358537222),
              f = v(f, p, c, s, n[d + 3], 16, -722521979),
              s = v(s, f, p, c, n[d + 6], 23, 76029189),
              c = v(c, s, f, p, n[d + 9], 4, -640364487),
              p = v(p, c, s, f, n[d + 12], 11, -421815835),
              f = v(f, p, c, s, n[d + 15], 16, 530742520),
              c = m(c, s = v(s, f, p, c, n[d + 2], 23, -995338651), f, p, n[d + 0], 6, -198630844),
              p = m(p, c, s, f, n[d + 7], 10, 1126891415),
              f = m(f, p, c, s, n[d + 14], 15, -1416354905),
              s = m(s, f, p, c, n[d + 5], 21, -57434055),
              c = m(c, s, f, p, n[d + 12], 6, 1700485571),
              p = m(p, c, s, f, n[d + 3], 10, -1894986606),
              f = m(f, p, c, s, n[d + 10], 15, -1051523),
              s = m(s, f, p, c, n[d + 1], 21, -2054922799),
              c = m(c, s, f, p, n[d + 8], 6, 1873313359),
              p = m(p, c, s, f, n[d + 15], 10, -30611744),
              f = m(f, p, c, s, n[d + 6], 15, -1560198380),
              s = m(s, f, p, c, n[d + 13], 21, 1309151649),
              c = m(c, s, f, p, n[d + 4], 6, -145523070),
              p = m(p, c, s, f, n[d + 11], 10, -1120210379),
              f = m(f, p, c, s, n[d + 2], 15, 718787259),
              s = m(s, f, p, c, n[d + 9], 21, -343485551),
              c = c + g >>> 0,
              s = s + b >>> 0,
              f = f + O >>> 0,
              p = p + w >>> 0
          }
          return r.endian([c, s, f, p])
      }
      )._ff = function(e, t, n, r, o, a, i) {
          var u = e + (t & n | ~t & r) + (o >>> 0) + i;
          return (u << a | u >>> 32 - a) + t
      }
      ,
      u._gg = function(e, t, n, r, o, a, i) {
          var u = e + (t & r | n & ~r) + (o >>> 0) + i;
          return (u << a | u >>> 32 - a) + t
      }
      ,
      u._hh = function(e, t, n, r, o, a, i) {
          var u = e + (t ^ n ^ r) + (o >>> 0) + i;
          return (u << a | u >>> 32 - a) + t
      }
      ,
      u._ii = function(e, t, n, r, o, a, i) {
          var u = e + (n ^ (t | ~r)) + (o >>> 0) + i;
          return (u << a | u >>> 32 - a) + t
      }
      ,
      u._blocksize = 16,
      u._digestsize = 16;
      return function(e, t) {
          if (null == e)
              throw new Error("Illegal argument " + e);
          var n = r.wordsToBytes(u(e, t));
          return t && t.asBytes ? n : t && t.asString ? i.bytesToString(n) : r.bytesToHex(n)
      }
  })();
