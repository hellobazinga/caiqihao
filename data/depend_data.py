#coding:utf-8
from util.operation_excel import OperationExcel
from base.runmethod import RunMethod
from data.get_data import GetData
from jsonpath_rw import jsonpath,parse
class Depend_data:
    def __init__(self,case_name):
        self.opera_excel = OperationExcel()
        self.data = GetData()
        self.case_name = case_name

    """通过case_id获取整行数据"""
    def get_case_line_data(self):
        rows_data = self.opera_excel.get_rows_data(self.case_id)
        return rows_data

    #执行依赖测试，获取结果
    def run_depend(self):
        run_method = RunMethod()
        row = self.opera_excel.get_row_num(self.case_name)
        url = self.data.get_url(row)
        method = self.data.get_request_method(row)
        header = self.data.get_header(row)
        request_data = eval(self.data.get_request_data(row))
        res = run_method.run_main(method,url,request_data,header)
        return res

    #根据依赖的key去获取执行依赖测试case
    def get_data_for_key(self,row):
        depend_data = self.data.get_data_depend(row)
        response_data = self.run_depend()
        jsonpath_exe = parse(depend_data)
        madle = jsonpath_exe.find(response_data)
        return [math.value for math in madle][0]
if __name__ == '__main__':
    depend_data = Depend_data('case1')
    data=depend_data.run_depend()
    print(data)


