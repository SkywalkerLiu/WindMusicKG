# -*- coding: utf-8 -*-
# @Time    : 2020/2/23 20:34
# @Author  : GaleHuang (Huang Dafeng)
# @github: https://github.com/Galehuang

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lxml import etree
from scrapy.selector import Selector
from ..items import BaikeSingerItem, UniqueNode
from scrapy_redis.spiders import RedisSpider
from Crawler.utils.Preprocess import extract_singer_names
from scrapy import Request
import re

BAIDUBAIKE_SERACH_URL = 'https://baike.baidu.com/search?word='
BAIDUBAIKE = 'https://baike.baidu.com'


class BaikeSpider(RedisSpider):
    name = 'MusicBaike'
    redis_key = 'MusicBaike:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(RedisSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        names = extract_singer_names(file='singers.json')
        for name in names:
            url = BAIDUBAIKE_SERACH_URL + name
            yield Request(url=url, callback=self.first_parse)

    def parse(self, response):
        return self.second_parse(response)

    # 负责处理百度百科的搜索结果，提取可能有用的百度百科页面链接
    def first_parse(self, response):
        dom = Selector(response)
        results = dom.xpath("//dl[@class='search-list']/dd")
        for result in results:
            summary = result.xpath("p[@class='result-summary']/text()").get()
            if re.search('歌手', summary) or re.search('乐队', summary) \
                    or re.search('组合', summary) or re.search('团体', summary):
                url = result.xpath("a[@class='result-title']/@href").get()
                if url[:4] != 'http':
                    url = BAIDUBAIKE + url
                yield Request(url=url, callback=self.second_parse, dont_filter=True)

    # 对可能有用的页面进行进一步筛选和正式信息提取
    def second_parse(self, response):
        item = BaikeSingerItem()
        dom = Selector(response)
        name = dom.xpath('//h1/text()').get()
        item['_name'] = name
        item['meta'] = dict()
        keys = dom.xpath('//dt[@class="basicInfo-item name"]/text()')
        keys = (x.get().replace("\xa0", '') for x in keys)
        keys = [x for x in keys]
        values = dom.xpath('//dd[@class="basicInfo-item value"]')
        for key, value in zip(keys, values):
            item['meta'][key] = process_values(value, key)
            if not len(item['meta'][key]):
                del item['meta'][key]
        item['url'] = response.request.url
        if '组合成员' in item['meta']:
            return item
        if '职业' not in item['meta']:
            return
        else:
            career = item['meta']['职业']
            match = False
            for candidate in {'歌手', '团体', '乐队', '音乐人', '音乐制作人', '制作人'}:
                res = re.search(candidate, career)
                if res:
                    match = True
                    break
            if not match:
                return
        return item


def process_values(value, key):
    if key in {"代表作品", "影视代表作"}:
        res = list()
        nodes = value.xpath("a")
        for node in nodes:
            temp = dict()
            temp["name"] = node.xpath("text()").extract_first().replace("\n", "")
            if not node.xpath("@href").extract_first():
                continue
            temp["url"] = "https://baike.baidu.com" + node.xpath("@href").extract_first()
            res.append(temp)
    elif key == "主要成就":
        res = value.xpath("text()").getall()
        res_awards = value.xpath("a[@target='_blank']/text()").getall()
        for i, str in enumerate(res):
            if str[-1] != '\n' and i != len(res) - 1 and res[i + 1][0] != '\n' and len(res_awards) != 0:
                str += res_awards[0]
                res[i] = str
                res_awards = res_awards[1:]
        achievements = ""
        for i in res:
            achievements += i
        achievements = achievements.split('\n')
        res = ' '.join(achievements)
    elif key in {"经纪公司", "毕业院校"}:
        res = value.xpath("text()").get().replace("\n", "")
        if res == "":
            res = dict()
            res["name"] = value.xpath("a/text()").get().replace("\n", "")
            res["url"] = "https://baike.baidu.com" + value.xpath("a/@href").get()
    else:
        res = value.xpath("text()").get().replace("\n", "")
        res = res.replace('\xa0', "")
        if res == "":
            res = value.xpath("a/text()").get()
            if not res:
                return ""
            res = res.replace("\n", "")
            res = res.replace('\xa0', '')
    return res
