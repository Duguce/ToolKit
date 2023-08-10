# -*- coding: utf-8  -*-
# @Author  : Yu Ching San 
# @Email   : zhgyqc@163.com
# @Time    : 2023/8/10 11:50
# @File    : comment_spider.py
# @Software: PyCharm
import concurrent.futures
import json
import logging
import random
import threading
import time

import pandas as pd
import requests
from fake_useragent import UserAgent

from config import comment_param, product_id

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


class JDCommentSpider:

    def __init__(self):
        self.comm_data = pd.DataFrame(
            columns=['user_id', 'user_name', 'content', 'create_time', 'score', 'location', 'product_id',
                     'product_name'])  # 商品评论数据
        self.comm_data_lock = threading.Lock()  # 线程锁
        self.product_id = product_id  # 商品id
        self.pages = comment_param['pages']  # 爬取的页数
        self.score = comment_param['score']  # 评分
        self.sort_type = comment_param['sort_type']  # 排序方式
        self.page_size = comment_param['page_size']  # 每页放置评论数

    def send_request(self, url):
        """
        发送请求
        :param url: 请求地址
        :param params: 请求参数
        :return: 响应结果
        """
        headers = {'user-agent': UserAgent().random}  # 随机生成请求头
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"请求失败，错误信息:{e}...")

    def get_comments(self, page):
        """
        获取商品评论
        :return: 响应结果
        """
        api_url = f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&' \
                  f'productId={self.product_id}&score={self.score}&sortType={self.sort_type}&page={page}&pageSize={self.page_size}&isShadowSku=0&fold=0&bbtf=&shield'
        response_data = self.send_request(api_url)
        logging.info(f"正在抓取商品ID为 {self.product_id} 的第 {page + 1} 页评论数据...")
        return response_data

    def parse_comments(self, response):
        """
        解析商品评论
        :param response: 响应结果
        :return: 商品评论
        """
        json_obj = json.loads(response)
        comments = json_obj['comments']
        comm_list = []  # 评论列表
        for comment in comments:
            user_id = comment['id']  # 用户id
            user_name = comment['nickname']  # 用户名
            content = comment['content']  # 评论内容
            create_time = comment['creationTime']  # 评论时间
            score = comment['score']  # 评分
            location = comment['location']  # 评论地区
            product_name = comment['referenceName']  # 商品名称
            comm_list.append(
                [user_id, user_name, content, create_time, score, location, self.product_id, product_name])  # 添加评论

        temp_df = pd.DataFrame(comm_list,
                               columns=['user_id', 'user_name', 'content', 'create_time', 'score', 'location',
                                        'product_id',
                                        'product_name'])  # 生成临时数据框

        return temp_df

    def save_comments(self, comm_data):
        """
        保存商品评论
        :param comm_data: 商品评论数据
        :return: None
        """
        comm_data.to_csv('./jd_comments.csv', index=False, encoding='utf-8-sig')
        logging.info(f"已保存商品ID为 {self.product_id} 的评论数据至文件...")

    def crawl_page(self, page):
        """
        爬取一页
        :param page: 页码
        :return: None
        """
        response = self.get_comments(page)
        comments = self.parse_comments(response)
        with self.comm_data_lock:
            self.comm_data = pd.concat([self.comm_data, comments], ignore_index=True)

        time.sleep(random.uniform(1, 3))

    def start_crawling(self):
        """
        开始爬取商品评论
        """
        logging.info(f"正在开始抓取商品ID为 {self.product_id} 的评论数据...")
        # 使用线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:  # 最大线程数为30
            for page in range(self.pages):  # 爬取pages页
                executor.submit(self.crawl_page, page)

        logging.info(f"已完成抓取商品ID为 {self.product_id} 的评论数据...")
        self.save_comments(self.comm_data)  # 保存数据
