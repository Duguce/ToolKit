# -*- coding: utf-8  -*-
import gensim
import numpy as np
import pandas as pd
import settings
import logging


def getWordVecs(wordList, model):
    """
    对输入的单词进行向量化，返回对应的向量信息
    :param wordList: 输入的特征词列表
    :param model: 训练好的词向量模型
    :return: 向量化的单词
    """
    vecs = []
    for w in wordList:
        w = w.replace('\n', '')
        try:
            vecs.append(model[w])
        except KeyError:
            continue
    return np.array(vecs, dtype="float")


def buildVecs(filename, model):
    """
    得到语料中所有单词向量的总和，然后取平均值作为模型的输入
    :param filename:语料内容
    :param model:训练好的词向量模型
    :return:向量化的语料信息
    """
    fileVecs = []
    with open(filename, 'rb') as contents:
        for line in contents:
            wordList = line.decode('utf-8').split(' ')
            vecs = getWordVecs(wordList, model)
            if len(vecs) > 0:
                vecsArray = sum(np.array(vecs)) / len(vecs)
                fileVecs.append(vecsArray)
    return fileVecs


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # 输入用于训练的词向量的语料集
    corpusPath = settings.staticDir + 'sgns.wiki.bigram-char'
    model = gensim.models.KeyedVectors.load_word2vec_format(corpusPath)
    model.save_word2vec_format('corpus.txt')
    # corpusPath = settings.staticDir + 'corpus.txt'
    # sentences = gensim.models.word2vec.Text8Corpus(corpusPath)
    # model = gensim.models.Word2Vec(sentences, hs=1, min_count=1, window=3, vector_size=100)  # 训练词向量模型
    # 将输入文本进行向量化
    pos_inputPath = settings.sourceData + 'pos_cut.txt'
    neg_inputPath = settings.sourceData + 'neg_cut.txt'
    posInput = buildVecs(pos_inputPath, model)
    negInput = buildVecs(neg_inputPath, model)
    # 将向量化后的正向文本和负向文本标注好情感倾向，并合并
    Y = np.concatenate((np.ones(len(posInput)), np.zeros(len(negInput))))
    X = posInput[:]
    for neg in negInput:
        X.append(neg)
    X = np.array(X)
    df_x = pd.DataFrame(X)
    df_y = pd.DataFrame(Y)
    # 输入向量化后的文本
    data = pd.concat([df_y, df_x], axis=1)
    outputPath = settings.sourceData + 'vecData.csv'
    data.to_csv(outputPath)
