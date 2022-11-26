# -*- coding: utf-8  -*-
import os

dstData_path = os.path.join(os.getcwd(), 'dstData')

IND_URL = "http://quote.eastmoney.com/center/boardlist.html#industry_board"  # 行情中心网页，可以看到所有行业列表
MAX_PAGE_IND = 5  # 行业列表网址的最大页码


START_DATE = "20150106"  # 爬取数据的起始日期，示例格式：20150106
END_DATE = "20221125"  # 爬取数据的截止日期，示例格式：20221125

STOCK_CODE = "601225"  # 目标爬取股票代码
STOCK_NAME = "陕西煤业"  # 目标爬取股票名称

IND_NAME = "煤炭行业"  # 需要爬取股票历史数据的行业名称
