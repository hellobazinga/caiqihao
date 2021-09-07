#coding:utf-8
import sys
sys.path.append(r'C:\pycharm\api-auto')
import HtmlTestRunner
import unittest
from base.runmethod import RunMethod
from data.get_data import GetData
from util.operation_excel import OperationExcel
from ddt import ddt,data
from data.depend_data import Depend_data
from util.commonUtil import CommonUtil
from util.send_email import  SendEmail
from main.run_main import RunTest

test_data = OperationExcel().get_data_value()
@ddt
class TestMethod(unittest.TestCase):
    def setUp(self):
        self.run_method = RunMethod()
        self.data = GetData()
        self.com_util = CommonUtil()
        self.send = SendEmail()
        self.pass_count = []
        self.fail_count = []
    @data(*test_data)
    def test_01(self,testdata):
        is_run = testdata['是否执行']

        if is_run == 'yes':
            case_id  = int(testdata['case_id'])
            url = testdata['url']
            method = testdata['请求方式']
            # 字符串转字典 eval()
            data = eval(testdata['请求数据'])
            header = testdata['header']
            expect = int(testdata['预期结果'])
            depend_case = testdata['depend_case']
            if 'case' in depend_case:
                self.depend_data = Depend_data(depend_case)
                # 获取依赖的返回数据
                depend_resopnse_data = self.depend_data.get_data_for_key(case_id)
                # 获取依赖的字段
                depend_key = self.data.get_depend_field(case_id)
                temp = eval(data["clientstr"])
                temp[depend_key] = depend_resopnse_data
                data["clientstr"] = str(temp)
            res = self.run_method.run_main(method,url,data)
            if self.assertEqual(res['messageCode'],1008):
                self.data.write_result(case_id, 'pass')
                self.pass_count.append(case_id)
            else:
                self.data.write_result(case_id,res)
                self.fail_count.append(case_id)



if __name__ == '__main__':
    #创建存放报告的文件
    filepath = '../report/htmlreport.html'
    fp = open(filepath,'wb')
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestMethod))
    runner = HtmlTestRunner.HTMLTestRunner(stream = fp,title = '测试报告')
    runner.run(suite)
    fp.close()
    user_list = ['1091335755@qq.com']
    run = RunTest()
    list = run.go_on_run()
    pass_list = list[0]
    fail_list = list[1]
    send = SendEmail()
    send.send_main(pass_list, fail_list,filepath)

