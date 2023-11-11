# JdSpider

京东评论&问答数据爬虫：根据商品Id实现对京东平台上的评论内容（目前仅支持爬取单个商品前100页的评论内容）及商品问答模块的问题数据

## 项目结构

```
│  comment_spider.py # 京东评论模块爬虫函数
│  config.py # 配置文件，可以通过修改本文件中的配置信息爬取所需要的数据
│  main.py # 主程序入口
│  qa_spider.py # 京东问答模块爬虫函数
│  README.md # 项目说明文档
│  test.py # 功能测试脚本
│
├─data # 爬取结果存储路径
│      jd_comments.xlsx # 爬取的评论数据示例
│      jd_qa.xlsx # 爬取的问答数据示例
```

## 安装依赖

Python 3.7+

```
pip install -r requirements.txt
```

## 待做功能

- [ ] 实现根据关键词从京东主页批量抓取商品ID；
- [ ] 实现批量抓取商品评论&问答数据逻辑。

