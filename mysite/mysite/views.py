from mysite.mysite.settings import *
import mysql.connector
from mysql.connector import errorcode
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse, redirect, render
import json


class db_connection():
    def __init__(self, mysql_host=MYSQL_HOST, mysql_port=MYSQL_PORT,
                 mysql_username=MYSQL_USERNAME, mysql_pass=MYSQL_PASS):

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

    def close(self):
        self.MysqlDB.close()


def Jaychou(request):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute("SELECT * from `singer` WHERE `baike_name` = '周杰伦'")
    res = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]
    conn.close()
    res = res[0]
    JayChou = dict()
    for i, column in enumerate(column_names):
        JayChou[column] = res[i]
    return render(request, 'Jaychou.html', {'singer': json.dumps(JayChou, ensure_ascii=False)})
