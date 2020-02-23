from errno import errorcode

from Storage.settings import *
import mysql.connector
from mysql.connector import errorcode

TABLES = dict()

TABLES['singer'] = (
    "CREATE TABLE `singer`("
    "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    "`baike_name` varchar(100) NOT NULL,"
    "`chinese_name` varchar(100) DEFAULT NULL,"
    "`english_name` varchar(100) DEFAULT NULL,"
    "`alias_name` varchar(100) DEFAULT NULL,"
    "`nationality` varchar(20) DEFAULT NULL,"
    "`ancestral_home` varchar(20) DEFAULT NULL,"
    "`nation` varchar(20) DEFAULT NULL,"
    "`constellation` varchar(30) DEFAULT NULL,"
    "`blood_type` varchar(30) DEFAULT NULL,"
    "`height` varchar(40) DEFAULT NULL,"
    "`weight` varchar(40) DEFAULT NULL,"
    "`birthplace` varchar(100) DEFAULT NULL,"
    "`birthdate` varchar(100) DEFAULT NULL,"
    "`company_id` int DEFAULT NULL,"
    "`career` varchar(40) DEFAULT NULL,"
    "`school_id` int DEFAULT NULL,"
    "`achievement` varchar(1000) DEFAULT NULL,"
    "`baike_url` varchar(200) NOT NULL,"
    "`create_time` varchar(40) NOT NULL,"
    "`update_time` varchar(40) NOT NULL,"
    "CONSTRAINT UC_singer UNIQUE(`baike_name`,`baike_url`)"
    ") ENGINE=InnoDB")

TABLES['song'] = (
    "CREATE TABLE `song`("
    "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    "`name` varchar(50) NOT NULL,"
    "`baike_url` varchar(200),"
    "`singer_id` int,"
    "`create_time` varchar(40) NOT NULL,"
    "`update_time` varchar(40) NOT NULL,"
    "CONSTRAINT UC_song UNIQUE(`name`,`baike_url`)"
    ") ENGINE=InnoDB"
)

TABLES['company'] = (
    "CREATE TABLE `company`("
    "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    "`name` varchar(50) NOT NULL,"
    "`baike_url` varchar(200),"
    "`create_time` varchar(40) NOT NULL,"
    "`update_time` varchar(40) NOT NULL,"
    "CONSTRAINT UC_company UNIQUE(`name`,`baike_url`)"
    ") ENGINE=InnoDB"
)

TABLES['school'] = (
    "CREATE TABLE `school`("
    "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    "`name` varchar(50) NOT NULL,"
    "`baike_url` varchar(200),"
    "`create_time` varchar(40) NOT NULL,"
    "`update_time` varchar(40) NOT NULL,"
    " CONSTRAINT UC_school UNIQUE(`name`,`baike_url`)"
    ") ENGINE=InnoDB"
)


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


cnx = mysql.connector.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS)
cursor = cnx.cursor()

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

sqls = ("ALTER TABLE `singer` ADD FOREIGN KEY(`company_id`) REFERENCES `company`(`id`)",
        "ALTER TABLE `singer` ADD FOREIGN KEY(`school_id`) REFERENCES `school`(`id`)",
        "ALTER TABLE `song` ADD FOREIGN KEY(`singer_id`) REFERENCES `singer`(`id`)")

for sql in sqls:
    print('Adding Foreign Key:', end='')
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print('OK')

cursor.close()
cnx.close()
