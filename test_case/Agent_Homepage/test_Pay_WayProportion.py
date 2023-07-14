import os
import pytest
import yaml
import re
yaml_file_path = os.path.join(os.path.dirname(__file__), "test_Pay_WayProportion.py.yaml")
with open(yaml_file_path, "r") as file:
    test_data = yaml.safe_load(file)

@pytest.mark.parametrize("test_data", [test_data])
def test_case(test_data):
    # 测试逻辑...

    # 获取yaml文件中的测试数据
    sql_queries = test_data.get("sql", [])
    for sql_query in sql_queries:
        # 使用正则表达式替换占位符
        sql_query = re.sub(r"\${yesterday_time\(\)}", "2023-07-13", sql_query)
        # 在这里执行SQL查询或其他操作
        # ...

    # 其他测试逻辑...