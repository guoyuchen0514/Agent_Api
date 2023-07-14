# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-02-16 15:49
# @Author : 皆人
# @File : yaml_control.py
# @Software: PyCharm
import os.path
import yaml
import logging

ERROR = logging.getLogger('error_logger')

class GetYamlData:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_yaml_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data
        except FileNotFoundError as e:
            ERROR.logger.error("找不到yaml文件：%s", e)
            raise
        except Exception as e:
            ERROR.logger.error("读取yaml文件出错：%s", e)
            raise

