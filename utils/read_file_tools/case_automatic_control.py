import os
import re
import datetime
import yaml
from utils.read_file_tools.yaml_control import GetYamlData

from utils.read_file_tools.get_yaml_data_analysis import CaseData


def ensure_path_sep(path):
    """确保路径中的分隔符为正确的格式"""
    return path.replace('/', os.path.sep).replace('\\', os.path.sep)


class CaseData:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_yaml_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data
        except Exception as e:
            print(f"读取yaml文件出错：{e}")
            raise

    # Rest of the code...


def write_testcase_file(*, allure_epic, allure_feature, class_title, func_title, case_path, case_ids, yaml_file_name,
                        allure_story, yesterday_time, testcase_file_name):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Rest of the code...


def get_testcase_content(yaml_file_path, yesterday_time):
    case_data = CaseData(ensure_path_sep('\\common\\config.yaml'))
    yaml_data = case_data.get_yaml_data()

    allure_epic = yaml_data['case_common']['allureEpic']
    allure_feature = yaml_data['case_common']['allureFeature']
    allure_story = yaml_data['case_common']['allureStory']

    class_title = case_data.case_process(case_id_switch=True)
    func_title = case_data.case_process(case_id_switch=True)
    case_ids = case_data.case_process(case_id_switch=True)

    case_dir = os.path.dirname(yaml_file_path)
    yaml_file_name = os.path.basename(yaml_file_path)
    case_file_name = os.path.splitext(yaml_file_name)[0]
    case_path = os.path.join(case_dir, '..', '..', 'test_case', f"test_{case_file_name}.py")
    testcase_file_name = f"test_{case_file_name}.py"

    write_testcase_file(
        allure_epic=allure_epic,
        allure_feature=allure_feature,
        class_title=class_title,
        func_title=func_title,
        case_path=case_path,
        case_ids=case_ids,
        yaml_file_name=yaml_file_name,
        allure_story=allure_story,
        yesterday_time=yesterday_time,
        testcase_file_name=testcase_file_name
    )


def generate_testcases(yaml_dir_path, yesterday_time):
    yaml_files = get_yaml_files(yaml_dir_path)
    for yaml_file in yaml_files:
        get_testcase_content(yaml_file, yesterday_time)


def get_yaml_files(yaml_dir_path):
    yaml_files = []
    for root, dirs, files in os.walk(yaml_dir_path):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                yaml_files.append(os.path.join(root, file))
    return yaml_files


if __name__ == '__main__':
    yaml_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    yesterday_time = str(datetime.date.today() - datetime.timedelta(days=1))
    generate_testcases(yaml_dir_path, yesterday_time)
