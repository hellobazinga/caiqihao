import xlrd
import xlwt
from xlutils.copy import copy
from util.connect_db import Connectdb_token
class OperationExcel:
    def __init__(self,file_name=None,sheet_id=None):
        self.conn = Connectdb_token()
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            self.file_name = '../case.xlsx'
            self.sheet_id = 0
        self.data = self.get_data()
    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables
    #获取单元格行数
    def get_lines(self):
        tables = self.data
        return tables.nrows
    #获取单元格内容
    def get_cell_value(self,row,col):
         return self.data.cell_value(row,col)

    #写入数据
    def write_value(self,row,col,value):
        read_data = xlrd.open_workbook(self.file_name)
        write_data = copy(read_data)
        sheet_data = write_data.get_sheet(0)
        sheet_data.write(row,col,value)
        write_data.save(self.file_name)

    #根据对应的case_id找到对应行的内容
    def get_rows_data(self,case_id):
        row_num = self.get_row_num(case_id)
        rows_data = self.get_row_values(row_num)
        return rows_data

    #根据对应的case_id找到对应的行号
    def get_row_num(self,case_name):
        num = 0
        cols_data = self.get_cols_data()
        for col_data in cols_data:
            if case_name in col_data:
                return num
            num = num +1
        return num

    #根据行号，找到该行的内容
    def get_row_values(self,row):
        tables = self.data
        row_data = tables.row_values(row)
        return row_data

    #获取某一列的内容
    def get_cols_data(self,col_id=None):
        if col_id != None:
            cols = self.data.col_values(col_id)
        else:
            cols = self.data.col_values(1)
        return cols
    #获取所有表格的内容
    def get_data_value(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        test_data = []
        for row in range(1, tables.nrows):
            sub_data = {}
            for col in range(0, tables.ncols):
                sub_data[self.get_cell_value(0, col)] = self.get_cell_value(row, col)
            test_data.append(sub_data)
        return test_data
    #修改所有token
    def change_token(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        data_num = 9
        temp_token  = eval(eval(self.get_cell_value(1,9))['clientstr'])['tempToken']
        for row in range(1, tables.nrows):
            data = self.get_cell_value(row,data_num)
            token = self.conn.get_token()
            data = data.replace(temp_token,token)
            self.write_value(row,data_num,data)
if __name__ == '__main__':
    opers = OperationExcel()
    print(opers.get_cols_data())