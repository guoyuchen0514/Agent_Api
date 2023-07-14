import datetime
import re
import os.path
from common.setting import ensure_path_sep
from utils.read_file_tools.yaml_control import GetYamlData
from utils.others_tool.exceptions import ValueNotFoundError



def write_case(case_path, page):
    with open(case_path, 'w', encoding='utf-8') as file:
        file.write(page)


def generate_testcase_content(file_name, yesterday_time, allure_epic, allure_feature, class_title, allure_story, func_title, case_ids):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    testcase_content = f"""
import allure
import pytest
from utils.read_file_tools.get_yaml_data_analysis import GetTestCase
from utils.read_file_tools.regular_control import regular
from utils.requests_tool.request_control import RequestControl
from utils.requests_tool.teardown_control import TearDownHandler
from utils.assertion.assertion_control import Assert
from utils.cache_process.redis_control import RedisHandler

case_ids = {case_ids}
TestData = GetTestCase.case_data(case_ids)
re_data = regular(str(TestData))

@allure.epic("{allure_epic}")
@allure.feature("{allure_feature}")
class Test{class_title}:

    @allure.story("{allure_story}")
    @pytest.mark.parametrize("in_data", eval(re_data), ids=[i["detail"] for i in TestData])
    def test_{func_title}(self, in_data, case_skip):
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(in_data["assert_data"]).assert_equality(response_data=res.response_data,
                                                       sql_data=res.sql_data, status_code=res.status_code)

if __name__ == "__main__":
    pytest.main(["{file_name}", "-s", "-W", "ignore:Module already imported:pytest.PytestWarning"])
""".strip()

    testcase_content = re.sub(r"\${{yesterday_time\(\)}}", yesterday_time, testcase_content)
    return testcase_content


def write_testcase_file(*, allure_epic, allure_feature, class_title, func_title, case_path, case_ids, file_name,
                        allure_story, yesterday_time):
    conf_data = GetYamlData(ensure_path_sep('\\common\\config.yaml')).get_yaml_data()
    real_time_update_test_cases = conf_data['real_time_update_test_cases']
    # 创建文件夹
    case_dir = os.path.dirname(case_path)
    os.makedirs(case_dir, exist_ok=True)

    testcase_content = generate_testcase_content(file_name, yesterday_time)

    # 执行正则表达式替换
    testcase_content = re.sub(r"\${yesterday_time\(\)}", yesterday_time, testcase_content)

    if real_time_update_test_cases:
        write_case(case_path=case_path, page=testcase_content)
    elif real_time_update_test_cases is False:
        if not os.path.exists(case_path):
            write_case(case_path=case_path, page=testcase_content)
    else:
        raise ValueNotFoundError('real_time_update_test_cases 配置不正确，只能配置True 或者False')


