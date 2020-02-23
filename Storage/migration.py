# -*- coding: utf-8 -*-
# @Time    : 2020/2/23 20:34
# @Author  : GaleHuang (Huang Dafeng)
# @github: https://github.com/Galehuang
# Migration data from Redis Database to MYSQL Database
import redis
import mysql.connector
import json
from Storage.settings import *
from mysql.connector import errorcode
from abc import abstractmethod


class Redis2Mysql(object):

    def __init__(self, redis_host=REDIS_HOST, redis_port=REDIS_PORT,
                 redis_pass=REDIS_PASS, mysql_host=MYSQL_HOST, mysql_port=MYSQL_PORT,
                 mysql_username=MYSQL_USERNAME, mysql_pass=MYSQL_PASS):
        self.RedisDB = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_pass)

        self.MysqlDB = mysql.connector.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_username,
            passwd=mysql_pass)
        mycursor = self.MysqlDB.cursor()

        try:
            mycursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Please set up your MYSQL database with setup.py first!")
                exit(1)
            else:
                print(err)
                exit(1)
        mycursor.close()

    def migrate(self):
        items = list()
        try:
            items = self.RedisDB.lrange('MusicBaike:items', 0, -1)
        except redis.AuthenticationError as err:
            print(err)
            print('[INFO]: The password or username for redis account is not correct!!!')
            raise redis.AuthenticationError
        for item in items:
            item = json.loads(item)
            self.process_item(item)

    @abstractmethod
    def synchronize(self):
        pass

    def process_item(self, item):
        school_id = 0
        company_id = 0
        singer_id = 0
        # 处理毕业院校
        if '毕业院校' in item['meta']:
            school_id = self.check_if_exists(item, 'school')
            if school_id:
                self.update_school_info(item, school_id)
            else:
                school_id = self.insert_school_info(item)

        # 处理经纪公司
        if '经纪公司' in item['meta']:
            company_id = self.check_if_exists(item, 'company')
            if company_id:
                self.update_company_info(item, company_id)
            else:
                company_id = self.insert_company_info(item)

        # 处理其他属性
        singer_id = self.check_if_exists(item, 'singer')
        if singer_id:
            self.update_singer_info(item, singer_id, school_id, company_id)
        else:
            singer_id = self.insert_singer_info(item, school_id, company_id)

        # 处理歌曲
        if '代表作品' in item['meta']:
            songs = item['meta']['代表作品']
            for song in songs:
                if self.check_if_exists(song, 'song'):
                    self.update_song_info(song)
                else:
                    self.insert_song_info(song, singer_id, item)

    def check_if_exists(self, item, table_name):
        sql = str()
        val = str()

        if table_name == 'singer':
            sql = "SELECT * FROM `singer` WHERE `baike_name`=%s AND `baike_url`=%s"
            val = (item['_name'], item['url'])

        elif table_name == 'school':
            school = item['meta']['毕业院校']

            if type(school) == str:
                sql = "SELECT * FROM `school` WHERE `name`=%s"
                val = (school,)
            else:
                sql = "SELECT * FROM `school` WHERE `name`=%s"
                val = (school['name'],)

            # if type(school) == str:
            #     sql = "SELECT * FROM `school` WHERE `name`=%s"
            #     val = (school,)
            # else:
            #     sql = "SELECT * FROM `school` WHERE `name`=%s AND `baike_url`=%s"
            #     val = (school['name'], school['url'])
        elif table_name == 'company':
            company = item['meta']['经纪公司']
            if type(company) == str:
                sql = "SELECT * FROM `company` WHERE `name`=%s"
                val = (company,)
            else:
                sql = "SELECT * FROM `company` WHERE `name`=%s"
                val = (company['name'],)

            # if type(company) == str:
            #     sql = "SELECT * FROM `company` WHERE `name`=%s"
            #     val = (company,)
            # else:
            #     sql = "SELECT * FROM `company` WHERE `name`=%s AND `baike_url`=%s"
            #     val = (company['name'], company['url'])
        elif table_name == 'song':
            sql = "SELECT * FROM `song` WHERE `name`=%s AND `baike_url`=%s"
            val = (item['name'], item['url'])
        else:
            print("Unknown table name {}!!".format(table_name))
            raise LookupError

        mycursor = self.MysqlDB.cursor()
        mycursor.execute(sql, val)
        res_id = mycursor.fetchall()
        if mycursor.rowcount:
            mycursor.close()
            return res_id[0][0]
        else:
            mycursor.close()
            return 0

    def insert_singer_info(self, item, school_id=None, company_id=None):
        sql = "INSERT INTO `singer`(`baike_name`,`baike_url`,`create_time`,`update_time`,"
        val = [item['_name'], item['url'], item['crawled'], item['crawled']]
        n = len(val)
        sql_s = "%s," * n

        if school_id:
            n += 1
            sql += 'school_id,'
            val.append(school_id)
            sql_s += "%s,"
        if company_id:
            n += 1
            sql += 'company_id,'
            val.append(company_id)
            sql_s += "%s,"
        for key in item['meta']:
            if key in RECORD_COLUMNS:
                n += 1
                sql += RECORD_COLUMNS[key] + ','
                val.append(item['meta'][key])
                sql_s += "%s,"
        if sql[-1] == ',':
            sql = sql[:-1]
        if sql_s[-1] == ',':
            sql_s = sql_s[:-1] + ')'
        # sql += ') VALUES (' + ('%s,' * (n - 1)) + '%s) '
        sql += ') VALUES (' + sql_s
        val = tuple(val)
        mycursor = self.MysqlDB.cursor()
        try:
            mycursor.execute(sql, val)
            self.MysqlDB.commit()
        except mysql.connector.Error as err:
            print('Error when inserting singer information:')
            print(err.msg)
            raise mysql.connector.Error
        else:
            print('Insert singer information successfully: name:{} url:{}'.format(item['_name'], item['url']))
            singer_id = mycursor.lastrowid
            print('The inserted singer ID: {}'.format(singer_id))
        self.MysqlDB.commit()
        mycursor.close()
        return singer_id

    def update_singer_info(self, item, singer_id, school_id=None, company_id=None):
        mycursor = self.MysqlDB.cursor()
        try:
            mycursor.execute("UPDATE `singer` set `update_time`=%s WHERE `id`=%s", (item['crawled'], singer_id))
        except mysql.connector.Error as err:
            print('Error when updating singer information singerID:{}'.format(singer_id))
            print(err.msg)
            raise mysql.connector.Error

        for key in item['meta']:
            if key in RECORD_COLUMNS:
                try:
                    sql = "UPDATE `singer` set " + RECORD_COLUMNS[key] + "=%s WHERE `id`=%s"
                    val = (item['meta'][key], singer_id)
                    mycursor.execute(sql, val)
                except mysql.connector.Error as err:
                    print('Error when updating singer information singerID:{}'.format(singer_id))
                    print(err.msg)
                    raise mysql.connector.Error

        sql_1 = "UPDATE `singer` SET `school_id`=%s WHERE `id` = %s"
        val_1 = (school_id, singer_id)
        sql_2 = "UPDATE `singer` SET `company_id`=%s WHERE `id` = %s"
        val_2 = (company_id, singer_id)
        try:
            if school_id:
                mycursor.execute(sql_1, val_1)
            if company_id:
                mycursor.execute(sql_2, val_2)
        except mysql.connector.Error as err:
            print('Error when updating singer information singerID:{} schoolID:{} '
                  'companyID:{}'.format(singer_id, school_id, company_id))
            print(err.msg)
            raise mysql.connector.Error
        else:
            print('Update singer information successfully: singerID:{} '.format(singer_id))
        self.MysqlDB.commit()
        mycursor.close()

    def insert_company_info(self, item):
        company = item['meta']['经纪公司']

        if type(company) == str:
            sql = "INSERT INTO `company` (`name`,`create_time`,`update_time`) VALUES (%s,%s,%s)"
            val = (company, item['crawled'], item['crawled'])
        else:
            sql = "INSERT INTO `company` (`name`,`baike_url`,`create_time`,`update_time`) " \
                  "VALUES (%s,%s,%s,%s)"
            val = (company['name'], company['url'], item['crawled'], item['crawled'])

        try:
            mycursor = self.MysqlDB.cursor()
            mycursor.execute(sql, val)
            self.MysqlDB.commit()
        except mysql.connector.Error as err:
            print('Error when inserting company information: {} {}'
                  .format(company['name'], company['url']))
            print(err.msg)
            raise mysql.connector.Error
        else:
            if not type(company) == str:
                print('Insert company information successfully: name:{} url:{}'.format(company['name'], company['url']))
            else:
                print('Insert company information successfully: name:{}'.format(company))
            company_id = mycursor.lastrowid
            print('The inserted company ID: {}'.format(company_id))

        self.MysqlDB.commit()
        mycursor.close()
        return company_id

    def update_company_info(self, item, company_id):
        mycursor = self.MysqlDB.cursor()
        company = item['meta']['经纪公司']

        if type(company) == str:
            return
        else:
            try:
                sql = "UPDATE `company` SET `baike_url`=%s, `update_time` = %s WHERE `id`=%s"
                val = (company['url'], item['crawled'], company_id)
                mycursor.execute(sql, val)
            except mysql.connector.Error as err:
                print('Error when updating company information:')
                print(err.msg)
                raise mysql.connector.Error
            else:
                print('Update company information: companyID:{} successfully!'.format(
                    company_id))
        self.MysqlDB.commit()
        mycursor.close()

    def insert_school_info(self, item):
        school = item['meta']['毕业院校']

        if type(school) == str:
            sql = "INSERT INTO `school` (`name`,`create_time`,`update_time`) VALUES (%s,%s,%s)"
            val = (school, item['crawled'], item['crawled'])
        else:
            sql = "INSERT INTO `school` (`name`,`baike_url`,`create_time`,`update_time`) " \
                  "VALUES (%s,%s,%s,%s)"
            val = (school['name'], school['url'], item['crawled'], item['crawled'])

        try:
            mycursor = self.MysqlDB.cursor()
            mycursor.execute(sql, val)
            self.MysqlDB.commit()
        except mysql.connector.Error as err:
            print('Error when inserting school information: {} {}'
                  .format(school['name'], school['url']))
            print(err.msg)
            raise mysql.connector.Error
        else:
            if not type(school) == str:
                print('Insert school information successfully: name:{} url:{}'.format(school['name'], school['url']))
            else:
                print('Insert school information successfully: name:{}'.format(school))
            school_id = mycursor.lastrowid
            print('The inserted school id: {}'.format(school_id))
        self.MysqlDB.commit()
        mycursor.close()
        return school_id

    def update_school_info(self, item, school_id):
        sql = ""
        val = ""
        school = item['meta']['毕业院校']
        if type(school) == str:
            return
        else:
            try:
                sql = "UPDATE `school` SET `baike_url`=%s, `update_time`=%s WHERE `id`=%s"
                val = (school['url'], item['crawled'], school_id)
                mycursor = self.MysqlDB.cursor()
                mycursor.execute(sql, val)
            except mysql.connector.Error as err:
                print('Error when updating school information: sql:{} val:{}'.format(sql, val))
                print(err.msg)
                raise mysql.connector.Error
            else:
                print('Update school information: schoolID:{} successfully!'.format(
                    school_id))
        self.MysqlDB.commit()
        mycursor.close()

    def insert_song_info(self, song, singer_id, item):
        sql = "INSERT INTO `song` (`name`,`baike_url`,`singer_id`,`create_time`,`update_time`) " \
              "VALUES (%s,%s,%s,%s,%s)"
        val = (song['name'], song['url'], singer_id, item['crawled'], item['crawled'])
        try:
            mycursor = self.MysqlDB.cursor()
            mycursor.execute(sql, val)
        except mysql.connector.Error as err:
            print('Error when inserting song information: sql:{} val:{}'.format(sql, val))
            print(err.msg)
            raise mysql.connector.Error
        else:
            print("Insert song information: name:{} url:{} successfully!!".format(song['name'], song['url']))
        self.MysqlDB.commit()
        mycursor.close()

    @abstractmethod
    def update_song_info(self, song):
        pass


MigrationTool = Redis2Mysql()
MigrationTool.migrate()
