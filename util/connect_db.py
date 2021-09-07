#coding:utf-8
import pymysql
from sshtunnel import SSHTunnelForwarder

class Connectdb_token:
    def get_token(self):
        with SSHTunnelForwarder(
            ('47.95.238.226',5220),  # 指定ssh登录的跳转机的address，端口号
            ssh_username='database',  # 跳转机的用户
            ssh_password='^43ys0$!Xu9k#rTP%N',# 跳板机用户的密码
            remote_bind_address=('rds3pz1l3efx8ty3d290399.mysql.rds.aliyuncs.com',3306)) as server: # mysql服务器的address，端口号
            conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                   port=server.local_bind_port,
                                   user='ia',  # 数据库用户名
                                   passwd='Data2015', # 数据库密码
                                   charset='utf8',
                                   db='investmentassistant',# 数据库名称
                                   autocommit=True)# 如果修改数据库自动提交
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM ia_onlineusermaster where uid = 19129912130 order by lastlogin desc limit 1")
            result=cursor.fetchall()
            df_result = result[0]
            token=df_result['TokenStr']
            cursor.close()#关闭游标
            conn.close()#关闭连接
        return token
if __name__ == '__main__':
    conn_token = Connectdb_token()
    print(conn_token.get_token())
