# coding:UTF-8
#!/usr/bin/python3

import requests
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import os
import re
import json


# 编辑下列信息
USER_ID   = '1650000'		# 学号
PASSWORD  = 'password'      # 密码
SEMESTER  = '20172'			# 学期
MAIL_HOST = 'smtp.qq.com'   # SMTP服务器
MAIL_USER = '10000@qq.com'  # 邮箱用户名
MAIL_PASS = 'mail_pwd'      # 邮箱密码
SENDER    = '10000@qq.com'  # 发件人
RECEIVER  = '10086@qq.com'  # 收件人
# 编辑上述信息

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +\
    '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
UPDATED = 'updated.json'

try:
    session = requests.Session()
    session.cookies.update({'User-Agent': UA})

    url_login = 'http://xuanke.tongji.edu.cn:443/oiosaml/saml/login'
    r = session.get(url_login)

    url_request = re.findall(r'url=(\S*)"></head>', r.text)[0]
    session.get(url_request)

    url_sso = 'https://ids.tongji.edu.cn:8443/nidp/saml2/sso?sid=0'
    session.post(url_sso)
    session.post(url_sso, data={
        'option': 'credential',
        'Ecom_User_ID': USER_ID,
        'Ecom_Password': PASSWORD,
        'submit': '登录'
    })
    r = session.get(url_sso)

    url_assert = 'http://xuanke.tongji.edu.cn:443/oiosaml/saml/SAMLAssertionConsumer'
    SAMLResponse = re.findall(
        r'name="SAMLResponse" value="(\S*)"/>', r.text)[0]
    session.post(url_assert, data={'SAMLResponse': SAMLResponse})

    url_redirect = 'http://xuanke.tongji.edu.cn/tj_login/redirect.jsp?' +\
        'link=/tj_xuankexjgl/score/query/student/cjcx.jsp?' +\
        'qxid=20051013779916$mkid=20051013779901&qxid=20051013779916'
    session.get(url_redirect)

    url_cjcx = 'http://xuanke.tongji.edu.cn/tj_xuankexjgl/score/query/' +\
        'student/cjcx.jsp?qxid=20051013779916&mkid=20051013779901'
    r = session.post(url_cjcx, data={
        'qx': '0',
        'xndxq': SEMESTER,
        'xklx': ''
    })
except:
    print('Error: 登录失败')
    exit()

html = etree.HTML(r.text)
table = html.xpath('//table[@class="mainTable"]/tr[td/div/font]')

os.chdir(os.path.dirname(os.path.abspath(__file__)))

updateList = []
with open(UPDATED, 'r') as fin:
    courseList = json.load(fin)

for tr in table:
    line = tr.xpath('td/div/font/text()')
    if line[0] in courseList:
        continue
    courseList.append(line[0])
    updateList.append('<td>' + '</td><td>'.join(line[1:4]) + '</td>')

with open(UPDATED, 'w') as fout:
    json.dump(courseList, fout)

if len(updateList):
    msgText = '<table border="1" rules="all"><tr>' + \
        '</tr><tr>'.join(updateList) + '</tr></table>'
    message = MIMEText(msgText, 'html', 'utf-8')
    message['From'] = formataddr([SENDER, SENDER])
    message['To'] = formataddr([RECEIVER, RECEIVER])
    message['Subject'] = Header('成绩更新%d' % len(courseList), 'utf-8')
    try:
        smtpObj = smtplib.SMTP(MAIL_HOST, 25)
        # smtpObj.set_debuglevel(1)
        smtpObj.login(MAIL_USER, MAIL_PASS)
        smtpObj.sendmail(SENDER, [RECEIVER], message.as_string())
        print('邮件发送成功')
    except smtplib.SMTPException:
        print('Error: 无法发送邮件')
else:
    print('没有成绩更新')
