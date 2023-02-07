import base64
import json
import random
import re
import time

import requests
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad

random.seed(time.time())

invisible = re.compile(
    r'[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]')


def iv_generate() -> str:
    date = time.localtime()
    year = str(date.tm_year)
    month = '{:0>2d}'.format(date.tm_mon)
    day = '{:0>2d}'.format(date.tm_mday)
    return year + month + day


def random_str(length: int) -> str:
    return ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))


# 字符串转二进制
def str_to_bin(s: str) -> str:
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


def encrypt(message: str, salt: str, iv: str) -> str:
    message = pad(message.encode(), DES3.block_size)
    salt = salt.encode()
    iv = iv.encode()
    encrypted = DES3.new(salt, DES3.MODE_CBC, iv).encrypt(message)
    encrypted = base64.b64encode(encrypted).decode()
    return encrypted


def decrypt(secret: str, key: str, iv: str = None) -> str:
    if iv is None:
        iv = iv_generate()
    secret = base64.b64decode(secret)
    key = key.encode()
    iv = iv.encode()
    decrypted = DES3.new(key, DES3.MODE_CBC, iv).decrypt(secret)
    decrypted = decrypted.decode()
    decrypted = re.sub(invisible, '', decrypted)
    return decrypted


def decrypt_response(resp: str) -> dict:
    resp = json.loads(resp)
    key = resp.get('secretKey')
    message = resp.get('result')
    iv = iv_generate()
    decrypted = decrypt(message, key, iv)
    return json.loads(decrypted)


def cipher() -> str:
    date = time.localtime()
    timestamp = str(int(time.time() * 1000))
    salt = random_str(24)
    iv = iv_generate()
    encrypted = encrypt(timestamp, salt, iv)
    ciphertext = salt + iv + encrypted
    return str_to_bin(ciphertext)
