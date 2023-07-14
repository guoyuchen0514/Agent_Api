# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-02-13 16:43
# @Author : 皆人
# @File : conftest.py
# @Software: PyCharm

import sys
import allure
import pytest
import ast
import requests

from  utils.cache_process.cache_control import CacheHandler
from utils.others_tool.models import TestCase
from utils.read_file_tools.regular_control import cache_regular
from utils.others_tool.allure_data.allure_tool import allure_step,allure_step_no


def get_login_token():
    url = 'https://api.pre.lianok.com/common/v1/user/login'
    header = {
        "content-type": "application/json"
    }
    data = {"phone":"15617886089","password":"zxc123456","type":"password","system":"agent"}

    res = requests.post(url=url, json=data, headers=header,verify=True)
    response_token =res.json()['data']['accessToken']
    CacheHandler.update_cache(cache_name='login_cookie',value=response_token)
get_login_token()


@pytest.fixture(scope="function", autouse=True)
def  case_skip(in_data):
    """处理跳过用例"""
    in_data = TestCase(**in_data)
    if ast.literal_eval(cache_regular(str(in_data.is_run))) is False:
        allure.dynamic.title(in_data.detail)
        allure_step_no(f"请求URL: {in_data.is_run}")
        allure_step_no(f"请求方式: {in_data.method}")
        allure_step("请求头: ", in_data.headers)
        allure_step("请求数据: ", in_data.data)
        allure_step("依赖数据: ", in_data.dependence_case_data)
        allure_step("预期数据: ", in_data.assert_data)
        pytest.skip()



