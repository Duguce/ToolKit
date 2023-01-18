# -*- coding: utf-8  -*-
import logging
import re

import pandas as pd

import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def loadDataSet(fileName):
    """
    读取数据
    @param fileName:文件名
    @return: 数据表
    """
    data = pd.read_csv(f'{config.sourceData}/{fileName}', encoding='utf-8')
    return data


def saveData(data, filename):
    """
    保存数据到csv文件
    @param data: 需要保存的数据
    @param filename: 保存数据的文件名
    @return:
    """
    data.to_csv(f'{config.dstData}/split_{filename}', encoding='utf_8_sig', index=False)


def cutCnSent(content):
    """
    对中文文本进行分句
    @param content:需要分句的原始文本
    @return:完成分句后的结果
    """
    content = re.sub('([。！？，\?])([^”’])', r"\1\n\2", content)
    content = re.sub('(\.{6})([^”’])', r"\1\n\2", content)
    content = re.sub('(\…{2})([^”’])', r"\1\n\2", content)
    content = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', content)
    content = content.rstrip()
    return content.split("\n")


def cutEnSent(content):
    """
    对英文文本进行分句
    @param content:需要分句的原始文本
    @return:完成分句后的结果
    """
    content = re.sub('([!?.";)(\?])([^”’])', r"\1\n\2", content)
    content = re.sub('(\.{6})([^”’])', r"\1\n\2", content)
    content = re.sub('(\…{2})([^”’])', r"\1\n\2", content)
    content = content.rstrip()
    return content.split("\n")


def main():
    filename = config.split_filename  # 需要分句的数据的文件名 
    data = loadDataSet(filename)
    logging.info(f'已读取文件 {filename}...')
    targetData = pd.DataFrame(  # 表头的标题信息
        columns=(
            'answer_number', 'question_title', 'author_name', 'answer_url', 'created_time', 'introduction', 'regional',
            'comment', 'comment_number'))
    comment_number = 0
    for index, row in data.iterrows():
        number, question_title, answer_url = row['序号'], row['问题'], row['地址']
        author_name, created_time = row['用户名'], row['回答时间']
        introduction, regional, content = row['用户介绍'], row['国籍信息'], row['回答内容']
        for comment in cutEnSent(content):
            comment_number += 1
            targetRow = {'answer_number': [number],
                         'question_title': [question_title],
                         'author_name': [author_name],
                         'answer_url': [answer_url],
                         'created_time': [created_time],
                         'introduction': [introduction],
                         'regional': [regional],
                         'comment': [comment],
                         'comment_number': [comment_number]
                         }
            targetData = targetData.append(pd.DataFrame(targetRow), ignore_index=True)
        logging.info(f'第{index + 1}条回答分句成功...')
    logging.info(f'共计得到{comment_number}条分句结果...')
    saveData(targetData, filename)
    logging.info(f'分句结果已保存至 split_{filename}...')


if __name__ == '__main__':
    main()
