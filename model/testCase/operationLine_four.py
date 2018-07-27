# coding:utf-8
__author__ = 'jiajia'
import unittest
from selenium import webdriver
from model.pages.login_page import loginIn
from time import sleep
from model.pages.getCargo_page import getCargo
from pymongo import MongoClient
import re
from model.common import log

'''
project:
1、使用深圳站点用户登陆
2、进入订单导入页面使用"虹桥快录"导入模板导入信息
3、进入输单页面对上一导入成功的单号进行输单补全操作
4、进入收货页面,对上一导入成功的单号进行子单信息补全操作
5、退出登陆
6、使用上海站点用户重新登陆
7、进入货物分拣页面对上单进行分拣操作
8、进入打单页面进行打单
'''
