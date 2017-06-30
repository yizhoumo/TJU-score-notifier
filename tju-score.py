#coding:UTF-8
#!/usr/bin/python3
import requests
import webbrowser
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import urllib
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
	id + '&IDToken2=' + urllib.quote(password)
check_url = 'http://xuanke.tongji.edu.cn/pass.jsp'
grade_url = 'http://xuanke.tongji.edu.cn/tj_login/redirect.jsp?link=/tj_xuankexjgl/score/query/student/cjcx.jsp?qxid=20051013779916$mkid=20051013779901&qxid=20051013779916'

# go and get grade!
session = requests.Session()
try:
	req1 = session.get(login_url, timeout=10)
	req2 = session.get(check_url, timeout=10)
except:
	print('Error: 网络连接失败')
	exit()

if not('失败' in req2.text):
	try:
		req3 = session.get(grade_url, timeout=10)
	except:
		print('Error: 网络连接失败')
		exit()

	text = req3.text
	html = etree.HTML(text)

	table = html.xpath('//table[@class="mainTable"]/tr[td/div/font]')

	file = open(sys.path[0] + '/tju-score.txt', 'a+')
	courseList = file.read().split()

	updateList = []

	for tr in table:
		line = tr.xpath('td/div/font/text()')
		if line[0] in courseList:
			continue
		courseList.append(line[0])
		file.write(line[0] + '\n')
		updateList.append('<td>' + '</td><td>'.join(line[1:4]) + '</td>')

	file.close()

	if len(updateList):
		msgText = '<table border="1" rules="all"><tr>' + '</tr><tr>'.join(updateList) + '</tr></table>'

		message = MIMEText(msgText, 'html', 'utf-8')
		message['From'] = formataddr([sender, sender])
		message['To'] = formataddr([receiver, receiver])
		message['Subject'] = Header('成绩更新'+str(len(courseList)), 'utf-8')

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
