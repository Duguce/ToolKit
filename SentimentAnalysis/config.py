import os

# 需要进行情感分析的原始数据集文件
filenames = ['datasets/20w标签_20wbiaoqian.csv',
             'datasets/20w标签_Sheet1.csv',
             'datasets/100w标签_100w标签.csv',
             'datasets/100w标签_Sheet1.csv']

# 将进行情感评分后的工作表保存到results文件夹
results_path = os.path.join(os.getcwd(), 'results')
