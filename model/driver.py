# -*- coding: UTF-8 -*-
import sys
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')

class plugIn(object):

    verificationErrors = []
    firefoxDriver = webdriver.Firefox(executable_path='/Users/xujiajia/Library/geckodriver')
    # url = "http://192.168.0.188:9988/LS"
    url = "http://192.168.1.79:8080/"
    # url = "http://ld.ldxpress.com"
    firefoxDriver.get(url)


