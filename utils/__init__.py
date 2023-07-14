# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-02-13 16:42
# @Author : 皆人
# @File : 1__init__.py.py
# @Software: PyCharm


from utils.read_file_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep
from utils.others_tool.models import Config

_data =GetYamlData(ensure_path_sep('\\common\\config.yaml')).get_yaml_data()
config =Config(**_data)


