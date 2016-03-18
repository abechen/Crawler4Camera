# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class Crawler4CameraItem(scrapy.Item):
    # define the fields for your item here like:
    source = Field()         # 資料來源
    memberId = Field()       # 會員帳號
    memberName = Field()     # 會員名稱
    crawlDateTime = Field()  # 爬蟲抓取時間
    postDateTime = Field()   # 商品文商上架時間
    title = Field()          # 商品文章標題
    href = Field()           # 商品文章連結
    articleId = Field()      # 商品文章編號
    price = Field()          # 商品價格
    location = Field()       # 商品所在地
    content = Field()        # 商品文章內文
