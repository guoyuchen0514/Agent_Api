# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-03-01 19:21
# @Author : 皆人
# @File : log_control.py
# @Software: PyCharm
import logging
from logging import handlers
from typing import Text
import colorlog
import time
from common.setting import ensure_path_sep


class LogHandler:
    """ 日志打印封装"""
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(
            self,
            filename: Text,
            level: Text = "info",
            when: Text = "D",
            fmt: Text = "%(levelname)-s%(asctime)s%(name)s:%(filename)s:%(lineno)d %(message)s"
    ):
        self.logger = logging.getLogger(filename)

        #设置日志颜色
        formatter = self.log_color()
        # 设置日志格式
        format_str = logging.Formatter(fmt)

        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往控制台上输出
        screen_output = logging.StreamHandler()
        # 设置控制台上显示的格式
        screen_output.setFormatter(formatter)
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        time_rotating = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=3,
            encoding='utf-8'
        )
        # 设置文件里写入的格式
        time_rotating.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(screen_output)
        self.logger.addHandler(time_rotating)
        self.log_path = ensure_path_sep('\\logs\\log.log')

    @classmethod
    def log_color(cls):
        """ 设置日志颜色 """
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'blue',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }

        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] - [%(name)s] - [%(levelname)s]: %(message)s',
            log_colors=log_colors_config
        )
        return formatter


now_time_day = time.strftime("%Y-%m-%d", time.localtime())
INFO = LogHandler(ensure_path_sep(f"\\logs\\info-{now_time_day}.log"), level='info')
ERROR = LogHandler(ensure_path_sep(f"\\logs\\error-{now_time_day}.log"), level='error')
WARNING = LogHandler(ensure_path_sep(f'\\logs\\warning-{now_time_day}.log'))

# if __name__ == '__main__':
#     INFO.logger.warning('测试')
#     ERROR.logger.error('error日志')
#     WARNING.logger.warning('warning日志')



