# -*- coding: utf-8  -*-
# @Author  : Duguce 
# @Email   : zhgyqc@163.com
# @Time    : 2022/12/25 19:09
# @File    : text_date_extraction.py
# @Software: PyCharm
# ============================================================ #
# 该脚本用于从文本中提取英文日期，并将其转换为标准格式
# '#506450933September 19, 2018 at 9:27:26 PM' ==> 2018-09-19
# ============================================================ #
import re
from datetime import datetime
import pandas as pd


def read_execl(file_path):
    # Read the entire Excel file into a DataFrame
    df = pd.read_excel(file_path)

    return df


def text_date_extraction(text):
    date_regex = r"([a-zA-Z]+) (\d{1,2}), (\d{4})"
    match = re.search(date_regex, text)

    # Extract the matched groups
    month = match.group(1)
    day = match.group(2)
    year = match.group(3)

    # Convert the date to a datetime object
    date_string = f"{year} {month} {day}"
    date = datetime.strptime(date_string, "%Y %B %d")
    # Format the date as YYYY-MM-DD
    formatted_date = date.strftime("%Y-%m-%d")

    return formatted_date


if __name__ == '__main__':
    # =================================================== #
    # # a little test case
    # test = "August 21, 2018"
    # text_date_extraction(test)

    # documents that need to be processed
    file_path = "[#pending_file#]"
    data = read_execl(file_path)
    created_time = data['created_time']
    date = []  # create a list to store standard format dates
    for d in created_time:
        try:
            date.append(text_date_extraction(d))
        except:
            date.append('')
    data['date'] = date
    # save the results to an Excel file
    data.to_excel('[#output_file#]')
