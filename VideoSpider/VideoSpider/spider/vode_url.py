# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/14 15:19
# File : vode_url.py

import asyncio
import aiohttp


async def get_url_dict(url: str, session: aiohttp.ClientSession) -> dict:
    """
    获取url，获取到的url是密文，后续还要加密一次
    :param url: 请求url
    :param session:会话保持
    :return: 字典格式 有一段js和url
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    async with session.get(url=url, headers=headers) as resp:
        return await resp.json()


if __name__ == '__main__':
    """"""
    url_ = "https://555dyx3.com/voddisp/id/421024/sid/4/nid/1.html"


    async def main():
        async with aiohttp.ClientSession(trust_env=True) as session:
            js = await get_url_dict(url=url_, session=session)
            print(js)


    asyncio.run(main())
