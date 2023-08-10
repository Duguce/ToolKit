# -*- coding: utf-8  -*-
# @Author  : Yu Ching San 
# @Email   : zhgyqc@163.com
# @Time    : 2023/8/10 11:53
# @File    : config.py
# @Software: PyCharm

product_id = 100038004397  # 商品id

comment_param = {
    'pages': 100,  # 爬取的页数（京东限制最多只能抓取100页）
    'score': 0,  # 评论类型（0：全部，3：好评，2：中评，1：差评）
    'sort_type': 6,  # 评论排序方式（5：推荐排序，6：时间排序）
    'page_size': 10,  # 每页显示多少条评论
}
