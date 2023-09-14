# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/14 16:31
# File : get_video_url.py

"""
获取m3u8的地址，这个地址是加密了的，后续还需要aes加密处理
"""

import asyncio

import aiohttp

from index_html import video_sid
from vode_url import get_url_dict


async def m3u8_url_ciphertext(url: str, session: aiohttp.ClientSession) -> str:
    """
    获取url,这个url就是获取m3u8的关键信息,这个是密文，不需要解密，后续还需要aes加密
    :param url: 请求url
    :param session:会话保持
    :return:
    """
    video_id, video_sid_, index_page = await video_sid(url=url, session=session)
    sid_url = "https://555dyx3.com/voddisp/id/%s/sid/%s/nid/1.html" % (video_id, video_sid_)
    js_dict = await get_url_dict(sid_url, session)
    video_url: str = js_dict.get("url")
    return video_url


if __name__ == '__main__':
    """"""
    url_1 = "https://555dyx3.com/vodplay/421024-6-1.html"


    async def main():
        async with aiohttp.ClientSession(trust_env=True) as session:
            video_sid_tuple = await m3u8_url_ciphertext(url=url_1, session=session)
            print(video_sid_tuple)


    asyncio.run(main())
