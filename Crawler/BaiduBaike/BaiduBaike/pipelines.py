# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
import json
from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread
from scrapy_redis.pipelines import RedisPipeline
from datetime import datetime

default_serialize = ScrapyJSONEncoder(ensure_ascii=False).encode
default_PIPELINE_KEY = '%(spider)s:items'
# 修复了Redis-cli中的中文显示乱码

class ChineseRedisPipeline(RedisPipeline):
    def __init(self,server,
                 key=default_PIPELINE_KEY,serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize = default_serialize

    def _process_item(self, item, spider):
        item["crawled"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        key = self.item_key(item, spider)
        data = default_serialize(item)
        self.server.rpush(key, data)
        return item




