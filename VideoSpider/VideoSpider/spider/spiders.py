# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/12 17:16
# File : spiders.py

"""下载图片类型的m3u8视频"""
import binascii
import os
from urllib.parse import urljoin
import asyncio

import aiofiles
from aiohttp import ClientSession
from Crypto.Cipher import AES

from VideoSpider.settings import INDEX_URL, SEMAPHORE_NUMBER, M3U8_DIR, MP4_DIR, USER_AGENT, SERVER_URL_PLAY
from VideoSpider.settings import RETRY, M3U8_ENCRYPT_DIR, M3U8_DECRYPT_DIR, HEADERS, SERVER_URL, REQUEST_TOKEN_URL
from VideoSpider.spider.m3u8_url import m3u8_url
from VideoSpider.log_config import *

logger = logging.getLogger(__name__)


def define_dir(dir_):
    # 判断目录是否存在，不存在则创建
    if not os.path.exists(dir_):
        # 判断存放ts的目录是否存在，不存在则创建
        os.makedirs(dir_)


class VideoSpider:
    def __init__(self):
        # 并发量
        self.semaphore = asyncio.Semaphore(value=SEMAPHORE_NUMBER)
        self.index_url = INDEX_URL
        self.file_number = 1
        define_dir(M3U8_DIR)
        define_dir(MP4_DIR)
        define_dir(M3U8_DECRYPT_DIR)
        define_dir(M3U8_ENCRYPT_DIR)

    async def aes_decrypt(self, key: bytes, iv_str: str, file_name: str) -> None:
        """
        aes解密
        :param key: aes key
        :param iv_str: aes iv
        :param file_name: 文件名称
        """
        # 解密后ts文件绝对地址
        decrypt_file_name = os.path.join(M3U8_DECRYPT_DIR, file_name)
        # 加密前ts文件绝对地址
        encrypt_file_name = os.path.join(M3U8_ENCRYPT_DIR, file_name)

        # 解密
        async with aiofiles.open(encrypt_file_name, "rb") as fe, aiofiles.open(decrypt_file_name, "wb") as fd:
            content = await fe.read()
            # iv = iv_str.replace("0x", "").encode()
            iv = binascii.unhexlify(iv_str.replace("0x", ""))

            aes = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
            new_content = aes.decrypt(content)
            await fd.write(new_content)  # 写入新文件
        logger.info("解密中....")

    async def get_m3u8(self, url: str, headers: dict, session: ClientSession, m3u8_flie_name: str) -> str:
        """
        下载m3u8文件
        :param url: url
        :param headers:headers
        :param session: session
        :param m3u8_flie_name: 文件名
        :return: 下载的m3u8文件本地地址
        """
        async with session.get(url=url, headers=headers) as resp:
            # m3u8文件地址
            m3u8_file_address = os.path.join(M3U8_DIR, m3u8_flie_name)
            async with aiofiles.open(m3u8_file_address, mode="wb") as f:
                # 下载m3u8文件
                await f.write(await resp.read())
                return m3u8_file_address

    async def ts_list_key(self, m3u8_file_address: str, m3u8_url) -> dict:
        """
        返回ts地址和加密文件
        :param m3u8_file_address:文件绝对地址
        :param m3u8_url: m3u8的url
        :return:
        """
        async with aiofiles.open(m3u8_file_address, mode='r') as f:
            ts_list_key_dick = {}
            ts_list = []
            key_url_iv_dict = {}
            async for line in f:
                # 清除两端空白字符
                m3u8_index: str = line.strip()
                if not m3u8_index.startswith("#"):
                    ts_url = m3u8_index
                    ts_list.append(ts_url)

                # 找到加密的地址
                # #EXT-X-KEY:METHOD=AES-128,URI="enc.key",IV=0x00000000000000000000000000000000
                if m3u8_index.startswith("#EXT-X-KEY:METHOD=AES-128,"):
                    # URI="enc.key",IV=0x00000000000000000000000000000000
                    enc_url_iv_str: str = m3u8_index.replace("#EXT-X-KEY:METHOD=AES-128,", '')
                    enc_url_iv_list: list = enc_url_iv_str.split(",")
                    # URI = "enc.key"
                    enc_url_str: str = enc_url_iv_list[0]
                    # 从双引号开始切割，切割到最后一个双引号
                    enc_url = enc_url_str[enc_url_str.index('"') + 1:enc_url_str.rindex('"')]

                    iv_str: str = enc_url_iv_list[1]
                    iv = iv_str.replace("IV=", "")
                    # 拼接url
                    key_url = urljoin(m3u8_url, enc_url)

                    key_url_iv_dict['key_url'] = key_url
                    key_url_iv_dict['iv'] = iv

            ts_list_key_dick["ts_list"] = ts_list
            ts_list_key_dick["key_url_iv_dict"] = key_url_iv_dict

            return ts_list_key_dick

    async def download_ts(self, url: str, headers: dict, session: ClientSession):
        """
        下载ts
        :param url: ts的url
        :param headers: 发生请求的headers
        :param session: aiohttp的session对象
        :return:
        """
        number = 0
        while 1:
            try:
                async with session.get(url=url, headers=headers) as resp:
                    # url : https://g.xlzyd.com:9999/hls/132/20230909/1886935/plist695.ts
                    # 文件名称
                    file_name: str = url.split("/")[-1]
                    # 文件地址
                    ts_path: str = os.path.join(M3U8_ENCRYPT_DIR, file_name)
                    async with aiofiles.open(ts_path, 'wb') as f:
                        # 写入数据
                        await f.write(await resp.read())
                        logger.info("下载第%d文件中..." % self.file_number)
                        self.file_number += 1
                break
            except Exception as e:
                logger.info("出错了，重试第%d次" % number)
                number += 1
                if number == RETRY:
                    break

    async def decrypt_ts_files(self, key: bytes, iv_str: str) -> None:
        """
        获取加密前文件夹下的所有ts文件
        :param key: aes key
        :param iv_str: aes iv
        """
        list_ts_files = []
        with os.scandir(M3U8_ENCRYPT_DIR) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.ts'):
                    list_ts_files.append(entry.name)

        await asyncio.wait(
            [asyncio.create_task(self.aes_decrypt(key, iv_str, file_name)) for file_name in list_ts_files])

    async def merge_ts(self, m3u8_file_address: str, ts_path: str, mp4_path: str, file_name: str = "视频.mp4") -> None:
        """
        视频合并
        :param m3u8_file_address: m3u8文件地址
        :param ts_path: 存放ts文件的文件夹路径
        :param mp4_path: 合并后的mp4存放路径
        :return:None
        """
        mp4_path = os.path.join(mp4_path, file_name)
        # 合并视频
        os.chdir(ts_path)  # 进入到ts文件夹 然后执行下面的命令
        # 创建合成视频的命令
        cmd = f"ffmpeg -f concat -safe 0 -i {m3u8_file_address} -c copy {mp4_path}"
        # cmd = f'ffmpeg -i {m3u8_file_address} -c copy {mp4_path}'
        # 执行命令
        # os.system(cmd) #
        os.popen(cmd)

    async def m3u8_file_path(self, file_name_path: str, ts_path: str) -> str:
        """
        根据下载下来的muu8文件修改为本地的m3u8文件
        :param ts_path: ts的免疫力
        :param file_name_path:m3u8文件路径
        :return:新的m3u8文件名称
        """
        new_file_name_path: str = os.path.join(M3U8_DIR, "new_index.m3u8")
        async with aiofiles.open(file_name_path, "r", encoding="UTF-8") as f1, \
                aiofiles.open(new_file_name_path, 'w', encoding="UTF-8") as f2:
            async for line in f1:
                if not line.startswith("#"):
                    line: str = line.strip()
                    line = line.split("/")[-1]
                    ts_line = os.path.join(ts_path, line)
                    ts_line = f"file '{ts_line}'\n"
                    await f2.write(ts_line)
            return new_file_name_path

    async def main(self):
        """主函数"""
        HEADERS["Host"] = "s.xlzys.com"
        async with ClientSession(trust_env=True) as session:

            # 获取m3u8地址
            m3u8_url_dict: dict = await m3u8_url(INDEX_URL, SERVER_URL_PLAY, SERVER_URL, REQUEST_TOKEN_URL, USER_AGENT,
                                                 session)
            m3u8_url_str = m3u8_url_dict.get("url")
            # 文件名称
            m3u8_file_name = m3u8_url_str.split("/")[-1]
            # m3u8文件绝对地址
            m3u8_file_address = await self.get_m3u8(m3u8_url_str, HEADERS, session, m3u8_file_name)
            # ts url和key iv
            ts_list_key_dict: dict = await self.ts_list_key(m3u8_file_address, m3u8_url_str)
            # print(ts_list_key_dict)
            ts_list: list = ts_list_key_dict.get("ts_list")
            key_url_iv_dict: dict = ts_list_key_dict.get("key_url_iv_dict")
            # 创建多个协成下载ts
            await asyncio.wait([asyncio.create_task(self.download_ts(url, HEADERS, session)) for url in ts_list])

            # 判断是否有加密，如果有就解密
            if key_url_iv_dict:
                # 如果有加密,先获取key
                key_url = key_url_iv_dict.get("key_url")
                iv_str = key_url_iv_dict.get("iv")
                async with session.get(url=key_url, headers=HEADERS) as resp:
                    key: bytes = await resp.read()
                # 解密所有文件
                await self.decrypt_ts_files(key, iv_str)

            # 判断是否有加密，有加密的放在另一个文件夹中的
            if key_url_iv_dict:
                # 有加密，去解密后的ts文件夹下
                ts_path = M3U8_DECRYPT_DIR
            else:
                # 没加密，加密前的ts文件夹下
                ts_path = M3U8_ENCRYPT_DIR

            # 修改m3u8文件里面的url
            new_m3u8_file_address: str = await self.m3u8_file_path(m3u8_file_address, ts_path)
            # 合并
            await self.merge_ts(new_m3u8_file_address, ts_path, MP4_DIR)

    def run(self):
        """启动函数"""
        # 3.10一下
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.main())

        # 3.10的
        asyncio.run(self.main())






if __name__ == '__main__':
    """"""
    video = VideoSpider()
    video.run()
