# -*- coding: utf-8  -*-
# @Author  : Yu Ching San 
# @Email   : zhgyqc@163.com
# @Time    : 2023/8/21 10:46
# @File    : qa_spider.py
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

from config import qa_param, DATA_PATH, MAX_WORKERS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


class JDQASpider:
    def __init__(self):
        self.pages = qa_param['pages']  # 爬取的页数
        self.product_id = qa_param['product_id']  # 商品id
        self.qa_data = pd.DataFrame(
            columns=['id', 'question_content', 'product_id', 'created_time', 'answer_id',
                     'answer_content', 'answer_created_time', 'location'])  # 商品问答数据
        self.qa_data_lock = threading.Lock()  # 线程锁
        self.data_path = DATA_PATH  # 数据存放路径
        self.max_workers = MAX_WORKERS  # 最大线程数

    def send_request(self, url):
        """
        发送请求
        :param url: 请求地址
        :param params: 请求参数
        :return: 响应结果
        """
        headers = {'user-agent': UserAgent().random}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"请求失败，错误信息:{e}...")

    def get_qa(self, page):
        """
        获取商品评论
        :return: 响应结果
        """
        api_url = f'https://api.m.jd.com/?appid=item-v3&' \
                  f'functionId=getQuestionAnswerList&page={page}&productId={self.product_id}'
        response_data = self.send_request(api_url)
        logging.info(f"正在抓取商品ID为 {self.product_id} 的第 {page} 页商品数据...")
        return response_data

    def parse_qa(self, response):
        """
        解析商品问答数据
        :param response: 响应结果
        :return: 商品问答数据
        """
        json_obj = json.loads(response)
        qa_data = json_obj['questionList']
        qa_list = []
        try:
            for qa in qa_data:  # 遍历每个问题
                id = qa['id']  # 问题id
                content = qa['content']  # 问题内容
                product_id = qa['productId']  # 商品id
                created_time = qa['created']  # 问题创建时间
                for answer in qa['answerList']:
                    answer_id = answer['id']
                    answer_content = answer['content']
                    answer_created_time = answer['created']
                    location = answer.get('location', 'None')
                    qa_list.append(
                        [id, content, product_id, created_time, answer_id, answer_content, answer_created_time,
                         location])
        except Exception as e:
            print(e)
        qa_df = pd.DataFrame(qa_list,
                             columns=['id', 'question_content', 'product_id', 'created_time', 'answer_id',
                                      'answer_content', 'answer_created_time', 'location'])

        return qa_df

    def save_data(self, qa_data):
        """
        保存商品评论
        :param comm_data: 商品评论数据
        :return: None
        """
        try:
            qa_data.to_excel(f"{self.data_path}\jd_qa.xlsx", index=False)
            logging.info(f"商品ID为 {self.product_id} 的商品问答数据保存至文件...")
        except Exception as e:
            logging.error(f"商品ID为 {self.product_id} 的商品问答数据保存失败，错误信息:{e}...")

    def crawl_page(self, page):
        """
        爬取一页
        :param page: 页码
        :return: None
        """
        response = self.get_qa(page)
        qa_data = self.parse_qa(response)
        with self.qa_data_lock:
            self.qa_data = pd.concat([self.qa_data, qa_data], ignore_index=True)

        time.sleep(random.uniform(3, 5))

    def start_crawling(self):
        """
        开始爬取商品问答数据
        """
        logging.info(f"开始爬取商品ID为 {self.product_id} 的商品问答数据...")
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for page in range(1, self.pages + 1):
                executor.submit(self.crawl_page, page)

        logging.info(f"商品ID为 {self.product_id} 的商品问答数据爬取完成...")
        self.save_data(self.qa_data)
