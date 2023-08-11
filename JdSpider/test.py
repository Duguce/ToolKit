# -*- coding: utf-8  -*-
# @Author  : Yu Ching San 
# @Email   : zhgyqc@163.com
# @Time    : 2023/8/10 18:09
# @File    : test.py
# @Software: PyCharm

import requests
from fake_useragent import UserAgent


headers = {'user-agent': UserAgent().random}
print(headers)