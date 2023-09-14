# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/12 17:12
# File : settings.py

import os

DIR = os.path.dirname(os.path.abspath(__file__))
M3U8_DIR = os.path.join(os.path.dirname(DIR), "m3u8_ts")
MP4_DIR = os.path.join(os.path.dirname(DIR), "mp4")

# 解密后的ts目录
M3U8_DECRYPT_DIR = os.path.join(M3U8_DIR, "decrypt_ts")

# 加密前的ts目录
M3U8_ENCRYPT_DIR = os.path.join(M3U8_DIR, "encrypt_ts")

# 某个视频页面的地址
INDEX_URL = "https://555dyx3.com/vodplay/421024-2-1.html"

APP_URL = 'www.555dy.com'
# UA
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
# headers
HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Origin": f"https://{APP_URL}",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    'User-Agent': USER_AGENT,
}

"""加密需要用到的url"""
# 获取m3u8的地址
SERVER_URL = 'https://player.ddzyku.com:3653/api'
SERVER_URL_PLAY = f'{SERVER_URL}/get_play_url'
# 加密需要的url
REQUEST_TOKEN_URL = 'https://zyz.sdljwomen.com'

# 协成并发量
SEMAPHORE_NUMBER = 1000

RETRY = 10

if __name__ == '__main__':
    print(M3U8_DECRYPT_DIR)
    print(M3U8_ENCRYPT_DIR)
