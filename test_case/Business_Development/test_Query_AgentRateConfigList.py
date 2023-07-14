import pytest
import yaml
import re
import datetime

@pytest.mark.parametrize("test_data", yaml.safe_load(open("test_Query_AgentRateConfigList.py.yaml")))
def test_case(test_data):
    # 获取yaml文件中的测试数据
    sql_queries = test_data.get("sql", [])
    for sql_query in sql_queries:
        # 使用正则表达式替换占位符
        sql_query = re.sub(r"\${yesterday_time\(\)}", "2023-07-13", sql_query)
        # 在这里执行SQL查询或其他操作
        # ...

    # 其他测试逻辑...