from common.setting import ensure_path_sep
from utils.read_file_tools.get_yaml_data_analysis import CaseData
from utils.read_file_tools.get_all_files_path import get_all_files
from utils.cache_process.cache_control import CacheHandler, _cache_config


def write_case_process():
    """
    获取所有用例，写入用例池中
    :return:
    """
    # 循环拿到所有存放用例的文件路径
    for i in get_all_files(file_path=ensure_path_sep("\\data"), yaml_data_switch=True):
        #循环读取文件中的数据
        case_process = CaseData(i).case_process(case_id_switch=True)
        if case_process is not None:
            # 转换数据类型
            for case in case_process:
                for k, v in case.items():
                    print(k,v)
                    # 判断 case_id 是否已存在
                    case_id_exit = k in _cache_config.keys()
                    """
                    return:bool
                    """
                    # 如果case_id 不存在，则将用例写入缓存池中
                    if case_id_exit is False:
                        CacheHandler.update_cache(cache_name=k, value=v)
                    # 当 case_id 为 True 存在时，则抛出异常,用例中不能有重复的case_id
                    elif case_id_exit is True:
                        raise ValueError(f"case_id: {k} 存在重复项, 请修改case_id\n"
                                         f"文件路径: {i}")
write_case_process()


