# -*- coding: utf-8  -*-
import requests
import json, os, time, random
from fake_useragent import UserAgent
import logging
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def get_html(url, encoding="utf-8"):
    logging.info(f"打开 {url}...")
    r = requests.get(url, headers={'user-agent': UserAgent().random}, stream=True)
    r.raise_for_status()
    r.encoding = encoding
    return r


def download_single_stock_data(stock_name, stock_code, start_date=config.START_DATE, end_date=config.END_DATE):
    """根据股票代码下载股票某日期范围内的数据"""
    if stock_code[0] in ["6", "9"]:
        stock_code = f"0{stock_code}"
    elif stock_code[0] in ["0", "3", "2"]:
        stock_code = f"1{stock_code}"
    download_chddata_api = f"http://quotes.money.163.com/service/chddata.html?code={stock_code}&start={start_date}&end={end_date}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
    chddata = get_html(download_chddata_api, encoding="gbk")
    f = open(f'{config.dstData_path}\\{config.IND_NAME}\\{stock_code}.csv', 'wb')
    for chunk in chddata.iter_content(chunk_size=1000000):
        if chunk:
            f.write(chunk)
    logging.info(f"股票 {stock_code}-{stock_name} 已爬取成功并保存...")


def read_json(filename):
    """读取json"""
    with open(f"{config.dstData_path}\\{filename}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_industry_stock_data(ind_name):
    """获取某一个行业所有的股票历史数据"""
    if not os.path.exists(f"dstData\\stockData-{ind_name}"):  # 创建一个以行业名命名的文件夹用于存储该行业的股票数据
        os.mkdir(f"stockData-\\{ind_name}")
    code_list = read_json(ind_name)
    logging.info(f"开始爬取 {ind_name} 行业的个股数据，共有 {len(code_list)} 只股票数据...")
    for stock_name in code_list:
        curr_code = code_list[stock_name]
        time.sleep(random.uniform(1, 2))
        download_single_stock_data(stock_name, curr_code)  # 下载对应的股票数据
    logging.info(f"{ind_name} 行业的 {len(code_list)} 只个股数据已全部爬取完成...")


if __name__ == '__main__':
    # download_single_stock_data(config.STOCK_NAME, config.STOCK_CODE)
    get_industry_stock_data(config.IND_NAME)
