# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-02-13 16:44
# @Author : 小熊
# @File : run.py
# @Software: PyCharm

import os
import pytest
from utils.others_tool.models import NotificationType
from utils.others_tool.allure_data.allure_report_data import AllureFileClean
from utils.logging_tool.log_control import INFO
# from utils.notify.wechat_send import WeChatSend
# from utils.notify.ding_talk import DingTalkSendMsg
# from utils.notify.send_mail import SendEmail
from utils.notify.lark import FeiShuTalkChatBot
# from utils.others_tool.allure_data.error_case_excel import ErrorCaseExcel
from utils import config


def run():
    # 从配置文件中获取项目名称
    try:
        INFO.logger.info(
            """
                       ,-,                      
                     ,' /                       
                   ,'  (          _          _  
           __...--'     `-....__,'(      _,-'/  
  _,---''''                     ````-._,'  ,'   
,'  o            杭州 火脸               `  <     
`.____  )))                          ...'  \    
   `--..._        .   .__....----''''   `-. \   
          ```7--i-`.  \                    `-`  
             `.(    `-.`.                       
               `'      `'                       
                  开始执行{}项目...
                """.format(config.project_name)
        )

        # 判断现有的测试用例，如果未生成测试代码，则自动生成
        # TestCaseAutomaticGeneration().get_case_automatic()

        pytest.main(['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                     '--alluredir', '.\\report\\tmp', "--clean-alluredir"]) #如果报告存在清楚它

        """
                   --reruns: 失败重跑次数
                   --count: 重复执行次数
                   -v: 显示错误位置以及错误的详细信息
                   -s: 等价于 pytest --capture=no 可以捕获print函数的输出
                   -q: 简化输出信息
                   -m: 运行指定标签的测试用例
                   -x: 一旦错误，则停止运行
                   --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
                    "--reruns=3", "--reruns-delay=2"
                   """

        os.system(r"allure generate .\report\tmp -o .\report\html --clean ") #-o报告内容放到指定文件夹下


        allure_data = AllureFileClean().get_case_count()
        notification_mapping = {
            # NotificationType.DING_TALK.value: DingTalkSendMsg(allure_data).send_ding_notification,
            # NotificationType.WECHAT.value: WeChatSend(allure_data).send_wechat_notification,
            # NotificationType.EMAIL.value: SendEmail(allure_data).send_main,
            NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
        }

        if config.notification_type != NotificationType.DEFAULT.value:
            notification_mapping.get(config.notification_type)()

        # if config.excel_report:
        #     ErrorCaseExcel().write_case()

        # 程序运行之后，自动启动报告，如果不想启动报告，可注释这段代码
        #  os.system(f"allure serve .\\report\\tmp -h 127.0.0.1 -p 9999")

    except Exception:
        # 如有异常，相关异常发送邮件
        # e = traceback.format_exc()
        # send_email = SendEmail(AllureFileClean.get_case_count())
        # send_email.error_mail(e)
        raise


if __name__ == '__main__':
    run()

if __name__ == '__main__':
    pytest.main()


