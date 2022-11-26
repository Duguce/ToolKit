# -*- coding: utf-8  -*-
import random, time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import logging
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def get_driver():
    """打开浏览器驱动"""
    logging.info("打开浏览器驱动...")
    firefox_profile = webdriver.FirefoxOptions()
    # 禁止图片和CSS加载，减小抓取时间
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    firefox_profile.set_preference('permissions.default.stylesheet', 2)
    s = Service("driver/geckodriver.exe")
    return webdriver.Firefox(service=s, options=firefox_profile)


def get_ind_url(url):
    """获取各行业股票列表网址"""
    url_dict_data = {}  # 定义字典用来存储行业股票列表网址
    driver = get_driver()
    driver.implicitly_wait(10)  # 隐式等待
    driver.get(url)
    logging.info(f"打开行业股票列表网址 {config.IND_URL}...")
    time.sleep(random.uniform(1, 2))
    for i in range(1, config.MAX_PAGE_IND + 1):  # 通过输入页码并点击实现翻页
        input_page = driver.find_element(By.CSS_SELECTOR, ".paginate_input")
        input_page.clear()  # 清空文本框中的元素
        input_page.send_keys(str(i))  # 传递对应的页码值
        input_click = driver.find_element(By.CSS_SELECTOR, ".paginte_go")
        input_click.click()  # 点击跳转按钮跳转到对应页面
        time.sleep(random.uniform(0.5, 1))
        industry = driver.find_element(By.CSS_SELECTOR, "table#table_wrapper-table > tbody")
        contents = industry.find_elements(By.TAG_NAME, "tr")  # 定位到行业信息列表
        for tr in contents:
            name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2) > a").text  # 获取行业名称
            href = f'http://data.eastmoney.com/bkzj/{tr.find_element(By.CSS_SELECTOR, "td:nth-child(2) > a").get_attribute("href")[-6:]}.html'  # 获取行业对于的股票详情页链接
            url_dict_data[name] = href
        logging.info(f"第 {i} 页行业股票列表网址已爬取完毕...")
    time.sleep(random.uniform(0.5, 1))
    driver.close()
    logging.info(f"行业股票列表网址已全部爬取成功，共计 {len(url_dict_data)} 个行业股票网址...")
    save_to_json(url_dict_data, "industry_list")  # 将数据保存至文件
    return url_dict_data


def get_stock_code(ind_url, ind_name):
    """获取某一行业所有个股的股票代码"""
    stock_code_data = {}  # 定义字典用来存储股票名称和代码
    driver = get_driver()
    driver.implicitly_wait(10)  # 隐式等待
    driver.get(ind_url)
    logging.info(f"打开 {ind_name} 行业股票详细信息网址 {ind_url}...")
    time.sleep(random.uniform(1, 2))
    is_one_page = driver.find_element(By.CSS_SELECTOR, "#dataview > div.dataview-pagination.tablepager").get_attribute(
        "style")
    if is_one_page == "display: none;":  # 如果只有一页内容时
        stocks = driver.find_element(By.XPATH, "//*[@id='dataview']/div[2]/div[2]/table/tbody")
        contents = stocks.find_elements(By.TAG_NAME, "tr")  # 定位到股票信息列表
        for tr in contents:
            code = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2) > a").text
            name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3) > a> span").text
            stock_code_data[name] = code
    else:
        max_page = driver.find_element(By.XPATH, "//*[@id='dataview']/div[3]/div[1]/a[last()-1]").text
        for i in range(1, int(max_page) + 1):  # 通过输入页码并点击实现翻页
            input_page = driver.find_element(By.CSS_SELECTOR, "#gotopageindex")
            input_page.clear()  # 清空文本框中的元素
            input_page.send_keys(str(i))  # 传递对应的页码值
            input_click = driver.find_element(By.CSS_SELECTOR,
                                              "#dataview > div.dataview-pagination.tablepager > div.gotopage > form > input.btn")
            input_click.click()  # 点击跳转按钮跳转到对应页面
            time.sleep(random.uniform(0.5, 1))
            stocks = driver.find_element(By.XPATH, "//*[@id='dataview']/div[2]/div[2]/table/tbody")
            contents = stocks.find_elements(By.TAG_NAME, "tr")  # 定位到股票信息列表
            for tr in contents:
                code = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2) > a").text
                name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3) > a> span").text
                stock_code_data[name] = code
    driver.close()
    logging.info(f"{ind_name} 股票代码已全部爬取成功，共计 {len(stock_code_data)} 个...")
    return stock_code_data


def save_to_json(data, filename="data"):
    """将数据保存为json文件格式"""
    with open(f"{config.dstData_path}\\{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    logging.info(f"数据已成功保存至 {filename}.json")


def read_json(filename):
    """读取json"""
    with open(f"{config.dstData_path}\\{filename}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_code(ind_lst):
    """获取所有行业的股票代码"""
    all_industry_stock = {}
    for n in ind_lst:
        u = ind_lst[n]
        data = get_stock_code(u, n)
        all_industry_stock.update(data)
    save_to_json(all_industry_stock, 'all_industry_stock_list')


if __name__ == '__main__':
    # get_ind_url(config.IND_URL)  # 获取各行业股票列表网址
    ind_lst = read_json('industry_list')
    # get_all_code(ind_lst) # 获取所有行业的股票代码获取所有行业的股票代码
    # 行业名称标准参见 http://quote.eastmoney.com/center/boardlist.html#industry_board
    ind_name = input("请输入需要获取个股代码列表的行业名称：\n")
    ind_url = ind_lst[ind_name]  # 获取行业个股列表的链接
    data = get_stock_code(ind_url, ind_name)  # 获取某一行业所有个股的股票代码
    save_to_json(data, ind_name)  # 将数据保存至文件
