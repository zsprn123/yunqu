# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/aes.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1371 bytes
import base64
from Crypto.Cipher import AES
_BLOCK_SIZE = 16
_PADDING = '{'
_pad = lambda s: s + (_BLOCK_SIZE - len(s) % _BLOCK_SIZE) * _PADDING
_encodeAES = lambda c, s: base64.b64encode(c.encrypt(_pad(s))).decode('utf-8')

def _decodeAES(c, e):
    e = e.encode('utf-8')
    decoded = base64.b64decode(e)
    decrypted = c.decrypt(decoded).decode('utf-8')
    return decrypted.rstrip(_PADDING)


_SECRET = '{\x82\xcc\xde\x03L\x1142\x9a\x94\xd6\xb1\xc5\xd4\xc6'
if len(_SECRET) > _BLOCK_SIZE:
    _SECRET = _SECRET[:_BLOCK_SIZE]
_cipher = AES.new(_SECRET)

def aes_encode(password):
    result = _encodeAES(_cipher, password)
    return result


def aes_decode(password):
    result = _decodeAES(_cipher, password)
    return result


__all__ = [
 'aes_encode', 'aes_decode']
# okay decompiling ./restful/hawkeye/common/aes.pyc
