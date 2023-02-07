import base64
import random
import time

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad

random.seed(time.time())


def random_str(length: int) -> str:
    return ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))


# 字符串转二进制
def str_to_bin(s: str) -> str:
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


def cipher() -> str:
    date = time.localtime()
    timestamp = str(int(time.time() * 1000))
    salt = random_str(24)
    year = str(date.tm_year)
    # 两位数month day
    month = '{:0>2d}'.format(date.tm_mon)
    day = '{:0>2d}'.format(date.tm_mday)
    iv = year + month + day
    encrypted = DES3.new(salt.encode(), DES3.MODE_CBC, iv.encode()).encrypt(pad(timestamp.encode(), DES3.block_size))
    encrypted = base64.b64encode(encrypted).decode()
    ciphertext = salt + iv + encrypted
    return str_to_bin(ciphertext)
