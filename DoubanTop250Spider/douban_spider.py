import requests
import random
import re
import config
import time
import pandas as pd


def get_html(link, encoding='utf-8'):
    r = requests.get(link, timeout=30, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Host': 'movie.douban.com'})
    r.raise_for_status()
    r.encoding = encoding
    return r.text


def db_spider(link):
    """
    Get the latest movies on the Top250 list from the link.
    :param link: douban Top250's link.
    :return: Scraped data.
    """
    time.sleep(random.random() * config.interval + config.interval)
    filmnames = re.findall('<a href=".*?">.*?<span class="title">(.*?)</span>', get_html(link), re.S)
    Englishnames = re.findall('<span class="title">.nbsp;/.nbsp;(.*?)</span>', get_html(link), re.S)
    Hongkongnames = re.findall('<span class="other">.nbsp;/.nbsp;(.*?)</span>', get_html(link), re.S)
    levels = re.findall('导演:(.*?).nbsp;.nbsp;.nbsp;主演:.*?', get_html(link), re.S)
    comments = re.findall('<span class="inq">(.*?)</span>', get_html(link), re.S)
    scores = re.findall('<span class="rating_num" property="v:average">(.*?)</span>', get_html(link), re.S)
    for filmname, Englishname, Hongkongname, level, comment, score in zip(filmnames, Englishnames, Hongkongnames,
                                                                          levels, comments, scores):
        movie = {
            'filmname': filmname,
            'Englishname': Englishname,
            'Hongkongname': Hongkongname,
            'level': level,
            'comment': comment,
            'score': score
        }
        movies_data.append(movie)


def export_to_excel(data, filename):
    # Convert the dict list to a DataFrame
    pf = pd.DataFrame(data)
    # Specifies the name of generated Excel table.
    file = pd.ExcelWriter(filename)
    # export.
    pf.to_excel(file, encoding='utf-8', index=False)
    # Save the data.
    file.save()


if __name__ == '__main__':
    movies_data = []
    for link in config.links:
        db_spider(link)
    export_to_excel(movies_data, config.filename)
    print(f'[NORMAL]   Successfully saved data to {config.filename}.')
