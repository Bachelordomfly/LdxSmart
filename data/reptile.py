# coding:utf-8
import requests
html = requests.get('http://www.ilyanglogis.com/functionality/zip_search_code.asp?zipcd=100-021')
print html.text
zipcode = u'100021'
now_code = u'SELJG'
count = len(zipcode)
if count == 6:
    zcode = zipcode[-6:-3] + u'-' + zipcode[-3:]
    url = 'http://www.ilyanglogis.com/functionality/zip_search_code.asp?zipcd=' + str(zcode)
    html = requests.get(url)
    t = html.text
    strlist = t.split('|')
    tip = []
    for value in strlist:  # 循环输出列表值
        tip.append(value)
    if now_code == tip[2]:
        print u'一洋分拣码获取正确'
    else:
        print u'一洋分拣码获取错误'
