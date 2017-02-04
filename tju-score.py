#coding:UTF-8
#!/usr/bin/python3
import requests
import webbrowser
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import sys
reload(sys)
sys.setdefaultencoding('utf8')

### 编辑下列信息
id = '1650000'          # 学号
password = '12345678'   # 密码
mail_host = 'smtp.qq.com'   # SMTP服务器
mail_user = '10000@qq.com'  # 邮箱用户名
mail_pass = '12345678'      # 邮箱密码
sender = '10000@qq.com'     # 发件人
receiver = '10000@qq.com'   # 收件人
### 编辑上述信息

login_url = 'http://tjis2.tongji.edu.cn:58080/amserver/UI/Login?service=adminconsoleservice&goto=http://tjis2.tongji.edu.cn:58080/amserver/base/AMAdminFrame&&IDToken1=' + \
    id + '&IDToken2=' + password
check_url = 'http://xuanke.tongji.edu.cn/pass.jsp'
grade_url = 'http://xuanke.tongji.edu.cn/tj_login/redirect.jsp?link=/tj_xuankexjgl/score/query/student/cjcx.jsp?qxid=20051013779916$mkid=20051013779901&qxid=20051013779916'

# go and get grade!
session = requests.Session()
req1 = session.request('GET', login_url)
req2 = session.request('GET', check_url)

if not('失败' in req2.text):

    req3 = session.request('GET', grade_url)
    text = req3.text
    html = etree.HTML(text)

    table = html.xpath('//table[@class="mainTable"]/tr[td/div/font]')
    nowCnt = str(len(table))
    cntFile = open('tju-score.txt', 'r')
    Cnt = cntFile.read()
    cntFile.close()

    if (Cnt != nowCnt):
        cntFile = open('tju-score.txt', 'w')
        cntFile.write(nowCnt)
        cntFile.close()
        result = []
        for tr in table:
            line = tr.xpath('td/div/font/text()')
            result.append('<td>' + '</td><td>'.join(line[1:4]) + '</td>')

        a = '<table border="1" rules="all"><tr>' + '</tr><tr>'.join(result) + '</tr></table>'

        message = MIMEText(a, 'html', 'utf-8')
        message['From'] = formataddr([sender, sender])
        message['To'] = formataddr([receiver, receiver])
        message['Subject'] = Header('成绩更新'+nowCnt, 'utf-8')

        try:
            smtpObj = smtplib.SMTP(mail_host, 25)
            #smtpObj.set_debuglevel(1)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, [receiver], message.as_string())
            print '邮件发送成功'
        except smtplib.SMTPException:
            print 'Error: 无法发送邮件'
    else:
        print('没有成绩更新')

else:
    print('Error: 登陆失败!')
