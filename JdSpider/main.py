# -*- coding: utf-8  -*-
# @Author  : Yu Ching San 
# @Email   : zhgyqc@163.com
# @Time    : 2023/8/10 11:50
# @File    : main.py
# @Software: PyCharm
from comment_spider import JDCommentSpider

if __name__ == '__main__':
    spider = JDCommentSpider()
    spider.start_crawling()
