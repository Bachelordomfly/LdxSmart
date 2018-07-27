# coding:utf-8
import unittest, time, HTMLTestRunner
from config.globalparameter import test_case_path, report_name
from model.common import send_email
'''
构建测试套件，并执行测试
'''


# 构建测试集,包含test_case目录下的所有以test开头的.py文件
# suite = unittest.defaultTestLoader.discover(start_dir=test_case_path,pattern='test*.py')
suite = unittest.defaultTestLoader.discover(start_dir=test_case_path, pattern='test_inputOrder.py')
# 执行测试
if __name__ == "__main__":
    report = report_name+"Report.html"
    fb = open(report, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fb,
        title=u'自动化测试报告',
        description=u'项目描述。………'
    )
    runner.run(suite)
    fb.close()
    # 发送邮件
    time.sleep(10)
    email = send_email.send_email()
    email.sendReport()
