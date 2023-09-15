# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/14 15:35
# File : index_html.py

import asyncio
import aiohttp
import ast
from lxml import etree
import random


async def random_sid(sid_list) -> tuple:
    # # 返回一个随机的视频视频解析列表，('421024', '2', 0)
    # return random.choice(sid_list)
    # 某些地址不一定能下载，暂时返回第三个
    return sid_list[2]


async def parse_video(html_data: str) -> list[tuple, ...]:
    """解析视频主页中的路线地址所需要的参数"""

    html_etree = etree.HTML(html_data)
    video_xpath_sid = "//div[@class='player-list']//*/@onclick"

    # ["change('421024','2',0)", "change('421024','7',0)", "change('421024','4',0)",]
    sid_list: list = html_etree.xpath(video_xpath_sid)

    # 去掉多余的数据，并且解析成列表套元组
    sid_list = [ast.literal_eval(i.replace("change", "")) for i in sid_list]

    # 第一个相当于视频id，第二个是解析的地址sid，第三个是第几个网页
    # [('421024', '2', 0), ('421024', '9', 0), ('421024', '4', 0), ('421024', '5', 0)]
    return sid_list


async def get_url(url: str, session: aiohttp.ClientSession) -> str:
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
        return await resp.text()


async def video_sid(url: str, session: aiohttp.ClientSession):
    html = await get_url(url=url, session=session)
    sid_list = await parse_video(html)
    return await random_sid(sid_list)


if __name__ == '__main__':
    """"""
    url_ = "https://555dyx3.com/vodplay/421024-6-1.html"


    async def main():
        async with aiohttp.ClientSession(trust_env=True) as session:
            video_sid_tuple = await video_sid(url=url_, session=session)
            print(video_sid_tuple)


    asyncio.run(main())
