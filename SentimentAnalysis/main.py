# -*- coding: utf-8 -*-
from pandas import read_csv
from snownlp import SnowNLP
import config
import pathlib


def sentiment_analysis(filename):
    """
    对评论内容进行情感预测
    情感极性值小于等于0.3的结果为负面情感结果
    情感极性值大于0.6的结果为正面情感结果
    正面情感的评论标签赋为1，负面情感的评论标签赋为-1，其他为中性赋为0
    :param filename: 需要进行情感分析的原始数据集文件
    :return: 标注情感得分的数据集
    """
    try:
        # 读取数据集
        dataset = read_csv(filename)
        comments = dataset['内容']
    except FileNotFoundError:
        pass
    else:
        sen_scores = []
        sen_label = []
        for comment in comments:
            s = SnowNLP(comment)
            sen_score = s.sentiments
            sen_score = float((format(sen_score, '.8f')))
            sen_scores.append(sen_score)
            if sen_score <= 0.3:
                sen_label.append(-1)
            elif sen_score > 0.6:
                sen_label.append(1)
            else:
                sen_label.append(0)
        # 保存分析结果
        p = pathlib.Path(filename)
        title = p.stem
        dataset['sen_scores'] = sen_scores
        dataset['sen_label'] = sen_label
        dataset.to_excel(f'{config.results_path}\sen_{title}.xlsx')


for filename in config.filenames:
    sentiment_analysis(filename)
