#!/usr/bin/python
# coding=utf-8

import urllib2
import cookielib
import urllib
from bs4 import BeautifulSoup
from prettytable import PrettyTable

'''上海大学绩点计算'''

# 验证码地址、post地址、成绩地址
PostUrl = "http://202.121.199.182:8080/pyxx/login.aspx"
CaptchaUrl = "http://202.121.199.182:8080/pyxx/PageTemplate/NsoftPage/yzm/createyzm.aspx"
gradeurl = "http://202.121.199.182:8080/pyxx/grgl/xskccjcx.aspx"
# 将cookies绑定到一个opener cookie由cookielib自动管理
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
# 用户名和密码
username = '15721540'
password = 'Jww930729'
# 用openr访问验证码地址,获取cookie
picture = opener.open(CaptchaUrl).read()
# 保存验证码到本地
with open('yzm.gif', 'wb') as pic:
    pic.write(picture)
    print "成功保存验证码"
# 打开保存的验证码图片 输入
SecretCode = raw_input('输入验证码： ')
print "你输入的验证码是%s" % SecretCode
# 要post的数据
postData = {
    '__VIEWSTATE': '/wEPDwUENTM4MWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgIFD2N0bDAwJENoZWNrQm94M\
    QUSY3RsMDAkSW1hZ2VCdXR0b24xkH0I/PAf6Xk+iNPAYCtn3PLjzYN6NykUQfqJW+LKcIY=',
    'ctl00$txtusername': username,
    'ctl00$txtpassword': password,
    'ctl00$txtyzm': SecretCode,
    'ctl00$CheckBox1': 'on',
    'ctl00$ImageButton1.x': 50,
    'ctl00$ImageButton1.y': 16,
}
# 根据抓包信息 构造表单
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleW\
              ebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
}
# 生成post数据 ?key1=value1&key2=value2的形式
data = urllib.urlencode(postData)
# 构造request请求
request = urllib2.Request(PostUrl, data, headers)
login_respones = opener.open(request)
print "login success!"

lesson_name = []
lesson_score = []
grade_respones = opener.open(gradeurl)
soup = BeautifulSoup(grade_respones, 'lxml')

for strings in soup.find_all("tr", class_="GridViewHeaderStyle"):
    for string_name in strings.stripped_strings:
        lesson_name.append(string_name)
x = PrettyTable(lesson_name)

for strs in soup.find_all("tr", class_="GridViewRowStyle"):
    for string_score in strs.stripped_strings:
        lesson_score.append(string_score)
    x.add_row(lesson_score)
    lesson_score = []
print x

for i in soup.find_all('span', id="MainWork_lblxwkpjcj"):
    print u"你的课程平均成绩为：" + i.string
