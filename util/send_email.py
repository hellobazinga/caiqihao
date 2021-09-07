#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class SendEmail:
    global send_user
    global email_host
    global password
    send_user = "qihao_cai@163.com"
    email_host = 'smtp.163.com'
    password = 'Aa8585569'
    def send_mail(self,user_list, sub, content,filepath):
        mail_mul = MIMEMultipart()
        user = "caiqihao"+"<"+send_user+">"
        f = open(filepath, 'rb')
        mail_body = f.read()
        f.close()

        #邮件正文
        message = MIMEText(content,_subtype='plain',_charset='utf-8')
        mail_mul['Subject'] = sub
        mail_mul['From'] = user
        mail_mul['To'] = ";".join(user_list)
        mail_mul.attach(message)
        #附件


        att = MIMEText(mail_body,'base64','utf-8')
        att['Content-Type'] = 'application/octet-stream'
        att['Content-Disposition'] = "attachment;filename = 'htmlreport.html'"
        mail_mul.attach(att)

        server = smtplib.SMTP()
        server.connect(email_host)
        server.login(send_user,password)
        server.sendmail(user,user_list,mail_mul.as_string())
        server.quit()

    def send_main(self, pass_list, fail_list,filepath):
        pass_num = float(len(pass_list))
        fail_num = float(len(fail_list))
        count_num = pass_num + fail_num
        pass_result = "%.2f%%" % (pass_num / count_num * 100)
        fail_result = "%.2f%%" % (fail_num / count_num * 100)
        user_list = ['1091335755@qq.com']
        sub = '接口自动化测试报告'
        content = '此次一共运行接口个数为%s个，其中通过个数为%s个，失败个数为%s，通过率为%s，失败率为%s' % (
        count_num, pass_num, fail_num, pass_result, fail_result)
        self.send_mail(user_list, sub, content,filepath)


if __name__ == '__main__':
    sen = SendEmail()
    file_path = '../report/htmlreport.html'
    user_list = ['1091335755@qq.com']
    sen.send_mail(user_list,'测测看',file_path)
