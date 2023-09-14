# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/14 18:55
# File : runserver.py
from VideoSpider.spider.spiders import VideoSpider

if __name__ == '__main__':
    """运行文件"""
    video = VideoSpider()
    video.run()
