# -*- coding: utf-8 -*-
# @Time    : 2020/2/23 20:34
# @Author  : GaleHuang (Huang Dafeng)
# @github: https://github.com/Galehuang

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..items import SingerItem


class NeteaseMusicSpider(CrawlSpider):
    name = "SingerCrawler"
    start_urls = ['https://music.163.com/#/discover/artist/cat?id={}&initial={}'.format(x, y)
                  for x in range(1001, 1004) for y in list(range(65, 91)) + [0]]

    # categories = {0:'华语男歌手',1:'华语女歌手',2:'华语组合/乐队'}
    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10,
                                  wait_until=EC.frame_to_be_available_and_switch_to_it((By.NAME, 'contentFrame')))

    def parse(self, response):
        dom = Selector(response)
        entries = dom.xpath('//div[@class="m-sgerlist"]/ul')
        if len(entries) == 0:
            return
        names = entries[0].xpath("//li/p/a/text()") + \
                entries[0].xpath('//li[@class="sml"]/a[@class="nm nm-icn f-thide s-fc0"]/text()')
        urls = entries[0].xpath("//li/p/a[@class='nm nm-icn f-thide s-fc0']/@href") + \
               entries[0].xpath('//li[@class="sml"]/a[@class="nm nm-icn f-thide s-fc0"]/@href')
        category = dom.xpath("//h3/span[@class='f-ff2 d-flag']/text()").extract_first()
        items = []
        for name, url in zip(names, urls):
            item = SingerItem()
            item['category'] = category
            item['name'] = name.get()
            item['url'] = 'https://music.163.com/#' + url.get().lstrip()
            items.append(item)
        return items
