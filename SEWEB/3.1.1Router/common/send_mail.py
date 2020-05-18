#! -*-conding:utf-8 -*-
#@Time: 2018/12/13 0013 17:51
#@swzhou
'''
发送邮件
'''

from email.mime.multipart import MIMEMultipart #多个文件类型
from email.mime.text import MIMEText    #txt类型文件/正文
from  email.mime.image import MIMEImage  #图片
from email.header import Header
from email import encoders
from email.utils import parseaddr,formataddr
import smtplib
import unittest


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

class sendMail(unittest.TestCase):

    def setUp(self):
        print('sendMail start')
        # pass


    def test_send_mail(self,filepath):
        from_addr = 'swzhou_autotest@163.com'
        password = '***'
        to_addr = ['***@utt.com.cn','***@qq.com']
        smtp_server = 'smtp.163.com'

        msg= MIMEMultipart('mixed') #多种文件声明邮件类型 “mixed"的邮件包含 纯文本正文，超文本正文，内嵌资源，附件
        #构造正文
        text = "hello, Automated Test Report Mail，send by Python.."
        text_plain = MIMEText(text,'plain','utf-8')
        msg.attach(text_plain)
        #设置邮件附件命名
        self.filepath = filepath
        filepath2 = filepath.split('\\')
        for i in filepath2:
            if 'html' in i:
                filename2 = i
        #构造附件
        # filename = r'C:/Users/swzhou/Desktop/web定位.txt'
        # sendfile = open(r'C:\Users\swzhou\Desktop\web定位.txt','rb').read()
        sendfile = open(filepath, 'rb').read()
        file = MIMEText(sendfile ,'base64','utf-8')
        file["Content-Type"] = 'application/octet-stream'
        file.add_header('Content-Disposition', 'attachment', filename=filename2) #可以重命名
        msg.attach(file)


        msg['From'] = format_addr('Autotest_email <%s>' % from_addr)
        msg['To'] = format_addr('Me <%s>' % to_addr)
        msg['Subject'] = Header('自动化测试邮件','utf-8').encode()


        #发送邮件
        server = smtplib.SMTP(smtp_server,25)
        server.set_debuglevel(1)
        server.login(from_addr,password)
        server.sendmail(from_addr,to_addr,msg.as_string())
        server.quit()

    def tearDown(self):
        print('sendMail over')

if __name__=='__main__':
    unittest.main()
