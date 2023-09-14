# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/14 11:02
# File : aes_e_d.py

import hmac
import binascii
from hashlib import md5, sha256

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


def get_keys():
    key = '55cc5c42a943afdc'.encode('utf-8')
    iv = 'd11324dcscfe16c0'.encode('utf-8')
    return key, iv


def encrypt_data(data_str):
    key, iv = get_keys()
    data = data_str.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data.hex().upper()


def decrypt_data(encrypted_data_str):
    key, iv = get_keys()
    encrypted_data = binascii.unhexlify(encrypted_data_str)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')


def md5_encrypt(input_string: str):
    # md5加密
    md5_hash = md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


def hmac_sha256(message, secret_key):
    message = message.encode('utf-8')
    secret_key = secret_key.encode('utf-8')
    signature = hmac.new(secret_key, message, digestmod=sha256).hexdigest()
    return signature
