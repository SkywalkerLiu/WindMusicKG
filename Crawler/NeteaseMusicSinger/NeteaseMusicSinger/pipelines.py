# -*- coding: utf-8 -*-
# @Time    : 2020/2/23 20:34
# @Author  : GaleHuang (Huang Dafeng)
# @github: https://github.com/Galehuang

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# Only for test, we use redis for caching in real
class SingerPipeline(object):
    def __init__(self):
        self.file = "singers.json"
        self.fp = open(self.file, 'w', encoding='utf-8')
        self.content = ""
        self.content += "[\n"

    def process_item(self, item, spider):
        self.content += json.dumps(dict(item),ensure_ascii=False)+",\n"
        return item

    def close_spider(self, spider):
        self.content = self.content[:-2]
        self.content += ']'
        self.fp.write(self.content)
        self.fp.close()