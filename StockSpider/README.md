# StockSpider

股票历史数据爬虫：根据股票代码爬取股票在某一日期范围内的历史数据，可以爬取单个股票数据，也可以批量爬取某个行业的股票数据（目前仅于深市和沪市的股票数据）

## 基本思路

> 目前该项目实现的基本思路是：首先，爬取[东方财富网](https://www.eastmoney.com/)的[行情中心页面](http://quote.eastmoney.com/center/boardlist.html#industry_board)的行业信息以及行业所对应的个股信息页面的链接；然后，在根据需要爬取某个行业的个股信息页面中每只股票的股票名称和股票代码（本项目是以[煤炭行业](http://data.eastmoney.com/bkzj/BK0437.html)为例），并将其保存为JSON文件格式；最后，通过请求[网易财经](http://money.163.com/)提供的个股历史数据接口下载所需要股票历史数据。

## 项目结构

```
│  config.py # 配置文件，可以通过修改本文件中的配置信息爬取所需要的数据
│  get_stock_code.py # 股票代码及股票名称爬取程序入口
│  main.py # 股票爬虫主程序，即个股历史数据爬取程序入口
│  README.md # 项目说明文档
│  requirements.txt
│
├─driver
│      chromedriver.exe # Chrome驱动
│      geckodriver.exe # gecko驱动
│
└─dstData # 该文件夹用于存储数据信息的文件
    │  industry_list.json # 行业信息以及行业所对应的个股信息页面的链接
    │  煤炭行业.json # 煤炭行业的个股信息列表（股票名称和股票代码）
    │
    └─stockData-煤炭行业 # 该文件夹用于存储煤炭行业的所有个股历史数据
```

## 安装依赖

Python 3.7+

```
pip install -r requirements.txt
```

## 说明备注

- 待做内容
  - [ ] 实现港股和美股的爬取功能；
  - [ ] 实现某个行业整体的股价波动历史数据的爬取功能；
  - [ ] 完善`get_industry_stock_data()`函数的功能，即实现一次性爬取所有行业的个股名称和对应代码。目前在爬取过程中会被挂掉，一种解决方法是增长休眠时间（不过这个方法太不优雅了），后续可以再改善一下。
- 浏览器驱动下载地址
  - Chrome：https://sites.google.com/chromium.org/driver/
  - Edge：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
  - Firefox：https://github.com/mozilla/geckodriver/releases
  - Safari：https://webkit.org/blog/6900/webdriver-support-in-safari-10/
- 项目地址：https://github.com/Duguce/ToolKit/tree/main/StockSpider

