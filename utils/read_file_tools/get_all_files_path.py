# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-02-28 15:01
# @Author : 皆人
# @File : get_all_files_path.py
# @Software: PyCharm
# get_all_files_path.py

import os

def get_all_files(file_path, yaml_data_switch=False) -> list:
    filename = []
    for root, dirs, files in os.walk(file_path):
        for file_name in files:
            path = os.path.join(root, file_name)
            if yaml_data_switch:
                if file_name.endswith(".yaml") or file_name.endswith(".yml"):
                    filename.append(path)
            else:
                filename.append(path)
    return filename





