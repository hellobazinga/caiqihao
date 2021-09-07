
import requests
import json
import sys
sys.path.append("C:/pycharm/api-auto")
from jsonpath_rw import jsonpath,parser
class RunMethod:
    def post_main(self,url,data,header=None):
        res = None
        if header != None:
            res = requests.post(url=url,data=data,headers=header).json()
        else:
            res = requests.post(url=url,data=data).json()
        return res
    def get_main(self,url,data=None,header=None):
        res = None
        if header != None:
            res = requests.get(url=url,data=data,headers=header).json()
        else:
            res = requests.get(url=url,data=data).json()
        return res
    def run_main(self,method,url,data,header=None):
        res = None
        if method =='POST':
            res = self.post_main(url,data,header)
        else:
            res= self.get_main(url,data,header)
        return res
if __name__ == '__main__':
    run = RunMethod()
    method = 'POST'
    url = 'https://dev.meix.com/InvestmentAssistant/team/getTeamList.do'
    data = {"clientstr":'{"showNum":20,"uid":"15159","companyCode":266,"token":"nozuonodie","currentPage":0}'}
    res = run.run_main(method,url,data)
    jsonpath_expr = parse('data[*].id')
    madle = jsonpath_expr.find(res)
    print([math.value for math in madle][0])
