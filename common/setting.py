# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-02-13 16:41
# @Author : 皆人
# @File : setting.py
# @Software: PyCharm

#配置环境变量
import os.path
from typing import Text
#
# BASH_PATH=os.path.dirname(__file__) #获取当前文件所在的目录
# BASH_PATH =BASH_PATH.replace('/','\\') #D:\pythonProject\pythonProject\Merchant_Api_Test\common repalce把\转成/
#
#
# DIR_PATH = os.path.dirname(os.path.dirname(__file__))#获取当前文件所在的上级目录
# DIR_PATH=DIR_PATH.replace('/','\\')  #D:\pythonProject\pythonProject\Merchant_Api_Test


#os.path.abspath(__file__))获取当前文件所在的绝对路径--->D:\Project\jieren_test\Merchant_Api_Test\common\setting.py
#os.path.dirname(os.path.abspath(__file__)) -->D:\Project\jieren_test\Merchant_Api_Test\commom
#os.path.dirname(os.path.dirname(os.path.abspath(__file__)))-->D:\Project\jieren_test\Merchant_Api_Test


def root_path():
    path =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path: Text)->Text:
    if '/' in path:
        path = os.sep.join(path.split("/"))
    if "\\" in path:
        path = os.sep.join(path.split("\\"))
    return root_path() +path



