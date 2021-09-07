import json
class OperationJson:
    def __init__(self):
        self.data = self.read_data()
    #读取json文件
    def read_data(self):
        with open("../test.json") as fp:
            data = json.load(fp)
            return data
    #根据关键字获取数据
    def get_data(self,id):
        return json.dumps(self.data[id])

if __name__ == '__main__':
    ope = OperationJson()
    print(ope.get_data('getTeamActivityList'))
