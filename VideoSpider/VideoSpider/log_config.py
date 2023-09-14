# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/8/31 15:52
# File : log_config.py
import logging

# 配置日志模块
logging.basicConfig(handlers=[logging.StreamHandler()], level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')

# 设置终端颜色
COLORS = {
    logging.DEBUG: '\033[00m',  # 默认颜色
    logging.INFO: '\033[92m',  # 绿色
    logging.WARNING: '\033[93m',  # 黄色
    logging.ERROR: '\033[91m',  # 红色
    logging.CRITICAL: '\033[91m\033[1m',  # 红色加粗
}


# 配置彩色日志格式
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage()
        if record.levelno in COLORS:
            record.color = COLORS[record.levelno]
        else:
            record.color = COLORS[logging.INFO]
            # 处理时间字符串
        time_str = self.formatTime(record)
        record.time = record.color + time_str + '\033[00m'  # 添加颜色代码和默认颜色代码
        record.levelname = record.levelname.capitalize()
        return super().format(record)


formatter = ColoredFormatter('%(time)s - %(color)s%(levelname)s - %(message)s\033[00m')
logging.getLogger().handlers[0].setFormatter(formatter)
logger = logging.getLogger(__name__)