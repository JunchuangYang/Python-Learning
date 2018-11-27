# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.exceptions import DropItem

# item 的处理
class TexrPipeline(object):
    def  __init__(self):
        self.limit=50
    def process_item(self, item, spider):
        if item['text']:
            if len(item['text'])>self.limit:
                item['text'] = item['text'][0:self.limit].rstrip()+'...'
                return  item['text']
        else :
            return DropItem('Missing Text')

# 保存到MongoDB


class MongoPipeLine(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db =mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return  cls(
            mongo_uri = crawler.setting.get('MONGO_URI'),
            mongo_db = crawler.setting.get('MONGO_DB')
        )

    # 爬虫启动时进行的相关操作
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # item插入到MongoDB
    def process_item(self,item,spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
