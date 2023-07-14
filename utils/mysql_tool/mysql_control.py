# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-03-09 18:17
# @Author : 皆人
# @File : mysql_control.py
# @Software: PyCharm
import pymysql
import datetime
from warnings import filterwarnings
from typing import Text,Union,List,Dict
from utils import config
import decimal
import  ast
filterwarnings("ignore", category=pymysql.Warning)
from utils.others_tool.exceptions import DataAcquisitionFailed,ValueTypeError
from utils.logging_tool.log_control import ERROR
from utils.read_file_tools.regular_control import cache_regular,sql_regular


class MysqlDB:
    if config.mysql_db.switch is True:
        def __init__(self):
            try:
                self.conn = pymysql.connect(
                    host = config.mysql_db.host,
                    user =config.mysql_db.user,
                    password =config.mysql_db.password,
                    port =config.mysql_db.port
                )

                self.cur =self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            except AttributeError as error:
                ERROR.logger.error("数据库连接失败，失败原因 %s" ,error)


        def execute(self,sql: Text):
            try:
                rows =self.cur.execute(sql)
                self.cur.fetchall()
                self.conn.commit()
                return rows
            except AttributeError as error:
                ERROR.logger.error("数据库连接失败，失败原因 %s",error)
                self.conn.rollback()
                raise
        def query(self, sql, state="all"):
            """
                查询
                :param sql:
                :param state:  all 是默认查询全部
                :return:
                """
            try:
                self.cur.execute(sql)

                if state == "all":
                    # 查询全部
                    data = self.cur.fetchall()
                else:
                    # 查询单条
                    data = self.cur.fetchone()
                return data
            except AttributeError as error_data:
                ERROR.logger.error("数据库连接失败，失败原因 %s", error_data)
                raise

        @classmethod
        def sql_data_handler(cls, query_data, data):
            """
            处理部分类型sql查询出来的数据格式
            @param query_data: 查询出来的sql数据
            @param data: 数据池
            @return:
            """
            # 将sql 返回的所有内容全部放入对象中
            for key, value in query_data.items():
                if isinstance(value, decimal.Decimal):
                    data[key] = float(value)
                elif isinstance(value, datetime.datetime):
                    data[key] = str(value)
                else:
                    data[key] = value
            return data

class SetUpMySQL(MysqlDB):
    """ 处理前置sql """

    def setup_sql_data(self, sql: Union[List, None]) -> Dict:
        """
            处理前置请求sql
            :param sql:
            :return:
            """
        sql = ast.literal_eval(cache_regular(str(sql)))
        try:
            data = {}
            if sql is not None:
                for i in sql:
                    # 判断断言类型为查询类型的时候，
                    if i[0:6].upper() == 'SELECT':
                        sql_date = self.query(sql=i)[0]
                        for key, value in sql_date.items():
                            data[key] = value
                    else:
                        self.execute(sql=i)
            return data
        except IndexError as exc:
            raise DataAcquisitionFailed("sql 数据查询失败，请检查setup_sql语句是否正确") from exc


class AssertExecution(MysqlDB):
    """ 处理断言 SQL 数据 """

    def assert_execution(self, sql: list, resp) -> dict:
        """
        执行 SQL，处理需要执行多条 SQL 的断言场景，最终将所有数据以对象形式返回
        :param sql: SQL
        :param resp: 接口响应数据
        :return: 断言结果
        """
        try:
            if isinstance(sql, list):
                data = {}
                _sql_type = ['UPDATE', 'update', 'DELETE', 'delete', 'INSERT', 'insert']
                if any(i in sql for i in _sql_type) is False:
                    for i in sql:
                        # 判断 SQL 中是否有正则，如果有则通过 JSONPath 提取相关的数据
                        sql = sql_regular(i, resp)
                        if sql is not None:
                            # 逐条处理断言 SQL
                            query_data = self.query(sql)
                            if query_data:
                                for key, value in query_data[0].items():
                                    # 如果字段值为空，则设置为默认值
                                    if value is None:
                                        query_data[0][key] = '0.00'
                                data.update(query_data[0])
                            else:
                                # 如果查询结果为空，设置字段内容为默认值
                                data['pay_amount'] = '0.00'
                                data['pay_count'] = '0'
                                data['commission'] = '0.00'
                        else:
                            raise DataAcquisitionFailed(f"该条 SQL 未查询出任何数据: {i}")
                else:
                    raise DataAcquisitionFailed("断言的 SQL 必须是查询的 SQL")
            else:
                raise ValueError("SQL 数据类型不正确，需要的类型是 list")
            return data  # 返回字典类型的断言结果
        except Exception as error_data:
            ERROR.logger.error("数据库连接失败，失败原因: %s", error_data)
            raise error_data










