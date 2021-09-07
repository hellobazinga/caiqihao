#coding:utf-8
import sys
sys.path.append("C:/pycharm/api-auto")
from base.runmethod import RunMethod
from data.get_data import GetData
from util.commonUtil import CommonUtil
from util.send_email import SendEmail
from data.depend_data import Depend_data
import json
class RunTest:
    def __init__(self):
        self.run_method = RunMethod()
        self.data = GetData()
        self.com_util = CommonUtil()
        self.send_mail = SendEmail()

    #程序执行的入口
    def go_on_run(self):
        res = None
        pass_count = []
        fail_count = []
        rows_count = self.data.get_case_lines()
        for i in range(1,rows_count):
            is_run = self.data.get_is_run(i)
            if is_run:
                url = self.data.get_url(i)
                method = self.data.get_request_method(i)
                #字符串转字典 eval()
                data = eval(self.data.get_request_data(i))
                header = self.data.get_header(i)
                expect = str(self.data.get_expect_data(i))
                depend_case = self.data.is_depend(i)
                if depend_case != None:
                    self.depend_data = Depend_data(depend_case)
                    #获取依赖的返回数据
                    depend_resopnse_data = self.depend_data.get_data_for_key(i)
                    #获取依赖的字段
                    depend_key = self.data.get_depend_field(i)
                    temp =  eval(data["clientstr"])
                    temp[depend_key] = depend_resopnse_data
                    data["clientstr"] = str(temp)
                res = json.dumps(self.run_method.run_main(method, url, data, header))
                if self.com_util.is_contain(expect,res):
                    self.data.write_result(i,'pass')
                    pass_count.append(i)
                else:
                    self.data.write_result(i,res)
                    fail_count.append(i)
        return [pass_count,fail_count]
if __name__ == '__main__':
    run = RunTest()
    list = run.go_on_run()
    print(list[0],list[1])
