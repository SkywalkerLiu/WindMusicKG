import os
import sys

import mysql.connector
from mysql.connector import errorcode

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)
from Storage.settings import *

TABLES = {'feedback': (
    "CREATE TABLE `feedback`("
    "`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    "`Message` varchar(500),"
    "`Email` varchar(100) NOT NULL,"
    "`qq` varchar(100),"
    "`Phone` varchar(30),"
    "`type` varchar(50),"
    "`create_time` varchar(40) NOT NULL"
    ") ENGINE=InnoDB"
)}


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

cursor.close()
cnx.close()
