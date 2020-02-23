# Scrapy settings for BaiduBaike project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['BaiduBaike.spiders']
NEWSPIDER_MODULE = 'BaiduBaike.spiders'

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

DUPEFILTER_DEBUG = True
ITEM_PIPELINES = {
    'BaiduBaike.pipelines.ChineseRedisPipeline':400,
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

# Unsafe! without password
REDIS_HOST = 'your_redis_host'
REDIS_PORT = 'your_redis_port'

# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.

# Safer, with password
#REDIS_URL = 'redis://user:pass@hostname:9001'


# 解决中文乱码
FEED_EXPORT_ENCODING = 'utf-8'