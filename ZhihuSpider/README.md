# ZhihuSpider
知乎爬虫：爬取知乎某一问题下的所有回答（回答数小于800左右）

## 基本思路

- 目前项目爬取的机制是将滚动条拉取到页面底端，然后一次性抓取所有的回答元素，但由于目前知乎的缓冲加载机制，当回答数量过多时(大概800左右)，前面的回答信息就抓取不到了；
  - 拟解决思路：边滚动边抓取（但不方便进行元素定位以避免重复抓取）

## 项目结构

```
│  config.py # 爬取链接及存储路径设置
│  README.md
│  requirements.txt
│  ZhihuSpider.py # 知乎爬虫主程序
│
├─Driver
│      chromedriver.exe # Chrome驱动
│      geckodriver.exe # gecko驱动
│
└─Results
        result-2022-07-28-深度神经网络DNN是否模拟了人类大脑皮层结构.csv # 抓取结果样例
```

## 安装依赖

Python 3.7+

```
pip install -r requirements.txt
```

## 使用方法

- 下载对应浏览器的驱动并置于[Driver](./Driver)文件夹==> 将需要爬取的问题链接置于<u>config.py</u>中 ==> 运行<u>ZhihuSpider.py</u>

## 抓取字段

| question_title | answer_url | author_name | fans_count | created_time | updated_time | comment_count | voteup_count |   content    |
| :------------: | :--------: | :---------: | :--------: | :----------: | :----------: | :-----------: | :----------: | :----------: |
|    问题名称    |  回答链接  |  作者昵称   |  粉丝数量  |   回答时间   | 最近修改时间 |   评论数量    |   赞同数量   | 回答文本内容 |

## 说明备注

- 项目地址：https://github.com/Duguce/ToolKit/tree/main/ZhihuSpider
