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

Step 1: 爬取网易云音乐歌手清单

```bash
cd Crawler/NeteaseMusicSinger
python run.py
```

运行完之后歌手的信息会保存在`singers.json`中

Step 2: 

1. 先将上一步爬取的`singers.json`放到`BaiduBaike`目录下

2. 配置redis服务器，将redis服务器相关参数填入`/Crawler/BaiduBaike/BaiduBaike/spiders/settings.py`中

3. 运行爬虫程序爬取百度百科歌手信息

   ```bash
   cd Crawler/BaiduBaike
   python run.py
   ```

   爬取的信息将自动保存到redis数据库中

Step 3:

将Redis数据库内容转移到MYSQL数据库中

1. 配置MYSQL服务器

2. 在`/Storage/settings.py`中填入MYSQL数据库和Redis数据库的相关参数

3. 在MYSQL数据库中建表

   ```bash
   cd Storage
   python setup.py
   ```

4. 运行迁移程序

   ```bash
   python migration.py
   ```

Step 4:

1. 在`mysite/mysite/settings.py`中填入MYSQL数据库的参数

2. 在MYSQL数据库中新建用户反馈表

   ```bash
   cd mysite/mysite
   python setup_feedback_table.py
   ```

3. 开启服务端

```bash
cd mysite/mysite
python manage.py 127.0.0.1:8000
```

Note: Step1, 2, 3和Step4的2都是可以直接跳过的, `Archive`文件夹里包含了这些几个步骤所得到的结果。

`Archive/singers.json:` 网易云音乐爬取结果

`Archive/dump.rdb:` 爬取得到的redis数据库内容

`Archive/windmusickg.sql:` 最终构建好的五张MYSQL表

