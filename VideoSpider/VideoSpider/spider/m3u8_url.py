# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/14 16:51
# File : m3u8_url.py

import asyncio
import json

import aiohttp
from aiohttp import ClientSession

from VideoSpider.spider.get_video_url import m3u8_url_ciphertext
from VideoSpider.spider.request_params import video_request_headers, video_request_params
from VideoSpider.urlits.aes_e_d import decrypt_data
from VideoSpider.settings import HEADERS, USER_AGENT


async def url_secret_key(ciphertext_url, url: str, server_url: str, request_token_url: str,
                         usera_gent: str, session: aiohttp.ClientSession):
    """m3u8的url"""

    aes_url_text = await m3u8_url_ciphertext(url=ciphertext_url, session=session)

    m3u8_headers = video_request_headers(aes_url_text, server_url)
    params = video_request_params(url=url, request_token_url=request_token_url, usera_gent=usera_gent)
    return m3u8_headers, params


async def m3u8_url(ciphertext_url: str, url: str, server_url: str, request_token_url: str,
                   usera_gent: str, session: ClientSession) -> dict:
    m3u8_headers, params = await url_secret_key(ciphertext_url, url, server_url, request_token_url, usera_gent, session)
    HEADERS["User-Agent"] = usera_gent
    headers = dict(HEADERS, **m3u8_headers)
    async with session.get(url=url, headers=headers, params=params) as resp:
        # 获得被加密的url字符串
        encrypt_data_url = await resp.text()
        # 解密，获得字符串
        url_json_str = decrypt_data(encrypt_data_url)
        # {'code': 200, 'data': {'url': 'https://s.xlzys.com/play/rb2Q7mja/index.m3u8'}}
        m3u8_url_: dict = json.loads(url_json_str)
        return m3u8_url_.get("data")


if __name__ == '__main__':
    """"""
    ciphertext_url = "https://555dyx3.com/vodplay/421024-6-1.html"
    server_url: str = 'https://player.ddzyku.com:3653/api'
    url: str = f'{server_url}/get_play_url'
    request_token_url: str = 'https://zyz.sdljwomen.com'

    async def main():
        async with aiohttp.ClientSession(trust_env=True) as session:
            m3u8_url_1 = await m3u8_url(ciphertext_url, url, server_url, request_token_url, USER_AGENT, session)
            print(m3u8_url_1)


    asyncio.run(main())
