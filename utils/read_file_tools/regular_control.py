# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-02-25 17:33
# @Author : 皆人
# @File : regular_control.py
# @Software: PyCharm

import datetime
import random
import re
import pymysql
from datetime import date, timedelta, datetime


from faker import Faker
from jsonpath import jsonpath

from utils.logging_tool.log_control import ERROR


class Context:
    """ 正则替换 """
    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    @classmethod
    def random_int(cls) -> int:
        """
        :return: 随机数
        """
        _data = random.randint(0, 5000)
        return _data

    def get_phone(self) -> int:
        """
        :return: 随机生成手机号码
        """
        phone = self.faker.phone_number()
        return phone





    def get_id_number(self) -> int:
        """
        :return: 随机生成身份证号码
        """

        id_number = self.faker.ssn()
        return id_number

    def get_female_name(self) -> str:
        """

        :return: 女生姓名
        """
        female_name = self.faker.name_female()
        return female_name

    def get_male_name(self) -> str:
        """
        :return: 男生姓名
        """
        male_name = self.faker.name_male()
        return male_name

    def get_email(self) -> str:
        """
        :return: 生成邮箱
        """
        email = self.faker.email()
        return email

    def get_db_data(sql):
        connect = pymysql.connect(host="121.41.215.125",
                                  port=3306, user="root",
                                  password="Youyun@baisi",
                                  db="platform_basic",
                                  charset="utf8")
        cur = connect.cursor()
        res = cur.execute(sql)
        data_all = cur.fetchall()
        return data_all


    @classmethod
    def self_operated_id(cls):
        """自营店铺 ID """
        operated_id = 212
        return operated_id

    @classmethod
    def get_time(cls) -> str:
        """
        计算当前时间
        :return:
        """
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time


    @classmethod
    def today_end_date(cls):
        """获取当天23:59:59秒的时间"""
        _today_end = date.today().strftime("%Y-%m-%d") + " 23:59:59"
        return _today_end

    @classmethod
    def today_date(cls):
        """获取今日0点整时间"""
        _today = date.today().strftime("%Y-%m-%d") + " 00:00:00"
        return str(_today)

    @classmethod
    def today_time(cls):
        """获取今天的日期"""
        _today_time =date.today().strftime("%Y-%m-%d")
        return str(_today_time)

    @classmethod
    def MonthFirstDay(self):
        """获取本月第一天"""
        _MonthFirstDay=datetime.now().strftime('%Y-%m')
        return '{}-01'.format(_MonthFirstDay)

    @classmethod
    def get_six_month_FirstDay(self,month_str=None):
        """获取前六个月的第一天"""
        if not month_str:
            month_str=datetime.now().strftime('%Y-%m')
        year,month=int(month_str.split('-')[0]),int(month_str.split('-')[1])
        if month == 6:
            year -= 1
            month = 12
        else:
            month-=6
        if month<10:
            month=str(month).zfill(2)
        return '{}-{}-01'.format(year, month)

    @classmethod
    def yesterday_time(cls):
        '''获取昨天的日期'''
        _today_time = date.today()
        _yesterday_time = _today_time - timedelta(days=1)
        return str(_yesterday_time)

    @classmethod
    def yesterday_end_date(cls):
        """获取昨日23:59:59秒的时间"""
        _yesterday_end = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")+ " 23:59:59"
        return _yesterday_end

    @classmethod
    def yesterday_date(cls):
        """获取昨日0点整时间"""
        _yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00"
        return str(_yesterday)

    @classmethod
    def pastthreedays_time(cls):
        '''获取近三天的日期'''
        _today_time = date.today()
        _pastthreedays_time = _today_time - timedelta(days=+3)
        return str(_pastthreedays_time)

    @classmethod
    def pastsevendays_time(cls):
        '''获取近七天的日期'''
        _today_time = date.today()
        _pastsevendays_time = _today_time - timedelta(days=+7)
        return str(_pastsevendays_time)

    @classmethod
    def pastsevendays_date(cls):
        """获取近七日0点整时间"""
        _pastsevendays = (date.today() - timedelta(days=+6)).strftime("%Y-%m-%d") + " 00:00:00"
        return str(_pastsevendays)

    @classmethod
    def pastthirtydays_time(cls):
        '''获取近三十天的日期'''
        _today_time = date.today()
        _pastthirtydays_time = _today_time - timedelta(days=+30)
        return str(_pastthirtydays_time)

    @classmethod
    def pastthirtydays_date(cls):
        """获取近三十日0点整时间"""
        _pastthirtydays = (date.today() - timedelta(days=+29)).strftime("%Y-%m-%d") + " 00:00:00"
        return str(_pastthirtydays)

    @classmethod
    def time_after_week(cls):
        """获取一周后12点整的时间"""
        _time_after_week = (date.today() + timedelta(days=+6)).strftime("%Y-%m-%d") + " 00:00:00"
        return _time_after_week

    @classmethod
    def host(cls) -> str:
        from utils import config
        """ 获取接口域名 """
        return config.host

    @classmethod
    def app_host(cls) -> str:
        from utils import config
        """获取app的host"""
        return config.app_host


def sql_json(js_path, res):
    """ 提取 sql中的 json 数据 """
    _json_data = jsonpath(res, js_path)[0]
    if _json_data is False:
        raise ValueError(f"sql中的jsonpath获取失败 {res}, {js_path}")
    return jsonpath(res, js_path)[0]



def sql_regular(value, res=None):
    """
    这里处理sql中的依赖数据，通过获取接口响应的jsonpath的值进行替换
    :param res: jsonpath使用的返回结果
    :param value:
    :return:
    """
    sql_json_list = re.findall(r"\$json\((.*?)\)\$", value)

    for i in sql_json_list:
        pattern = re.compile(r'\$json\(' + i.replace('$', "\$").replace('[', '\[') + r'\)\$')
        key = str(sql_json(i, res))
        value = re.sub(pattern, key, value, count=1)

    return value


# {'errorCode': {'jsonpath': '$.errorCode', 'type': '==', 'value': -1, 'AssertType': None}}

def cache_regular(value):
    from utils.cache_process.cache_control import CacheHandler
    """  
    通过正则的方式，读取缓存中的内容
    # 例：$cache{login_init}
    # :param value:
    # :return:
    # 正则获取 $cache{login_init}中的值 --> login_init
    """
    regular_dates = re.findall(r"\$cache{(.*?)}", value)
    # 拿到的是一个list，循环数据
    for regular_data in regular_dates:
        value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
        if any(i in regular_data for i in value_types) is True:
            value_types = regular_data.split(":")[0]
            regular_data = regular_data.split(":")[1]
            # pattern = re.compile(r'\'\$cache{' + value_types.split(":")[0] + r'(.*?)}\'')
            pattern = re.compile(r'\'\$cache{' + value_types.split(":")[0] + ":" + regular_data + r'}\'')
        else:
            pattern = re.compile(
                r'\$cache{' + regular_data.replace('$', "\$").replace('[', '\[') + r'}'
            )
        try:
            cache_data = CacheHandler.get_cache(regular_data)
            # 使用sub方法，替换已经拿到的内容
            value = re.sub(pattern, str(cache_data), value)
        except Exception:
            pass
    return value





def regular(target):
    try:
        regular_pattern = r"\${{(.*?)}}"
        while re.findall(regular_pattern, target):
            key = re.search(regular_pattern, target).group(1)
            value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
            if any(i in key for i in value_types):
                func_name = key.split(":")[1].split("(")[0]
                value_name = key.split(":")[1].split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(Context(), func_name)()
                else:
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                target = re.sub(regular_pattern, str(value_data), target, 1)
            else:
                func_name = key.split("(")[0]
                value_name = key.split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(Context(), func_name)()
                else:
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                target = re.sub(regular_pattern, str(value_data), target, 1)
        return target
    except AttributeError:
        ERROR.logger.error("未找到对应的替换的数据，请检查数据是否正确：%s", target)
        raise


# if __name__ == '__main__':
#     a='${{host()}}'
# #     # a='${{host()}}'
# #     # a = {'a':'${{int:random_int()}}'}
#     a={'a':'${{int:random_int()}}'}
#     b = regular(str(a))
#     print(b)
#     print(type(b))



