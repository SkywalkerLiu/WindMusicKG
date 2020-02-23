# WindMusicKG

华语流行音乐歌手图谱：轻量级demo

## 基本框架

1. 利用爬取的半结构化数据构建华语歌手知识图谱，支持网页端可视化、搜索和后台管理等功能
2. 通过Scrapy-redis分布式爬虫框架、Selenium插件以及lxml解析工具获取数据来源
3. 采用MySQL数据库存储三元组，编写了迁移模块将数据迁移到MYSQL数据库
4. 使用Django+Echarts做服务端和图谱可视化

## 项目文件描述

### Crawler

数据来源：

1. 利用网易云音乐爬取歌手列表
2. 利用百度百科获取歌手详细信息

爬虫模块：

`/Crawler/NeteaseMusicSinger:` 用来爬取网易云音乐的华语歌手/乐队的列表，爬取下来的歌手信息保存在`singers.json`文件中

`/Crawler/BaiduBaike:` 用来根据歌手名爬取对应的歌手的百度百科信息，采用`Scrapy-redis`分布式爬虫框架，爬取的歌手信息以JSON字符串形式保存在redis数据库中

`/Crawler/BaiduBaike/BaiduBaike/spiders/settings.py:` 设置redis数据库等配置信息

### Storage

存储模块

`/Storage/setup.py:` 初始化四张MYSQL表，分别用来存储歌手、经纪公司、毕业院校和歌曲信息

`/Storage/migration.py:` 将数据从Redis数据库中迁移到MYSQL数据库中

`/Storage/settings.py:` 配置Redis数据库和MYSQL数据库等配置信息

### mysite

服务端和图谱可视化

`/mysite/mysite/settings.py` 配置MYSQL数据库等信息

## 使用方法

待补充

