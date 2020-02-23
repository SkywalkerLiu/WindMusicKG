from mysite.mysite.settings import *
import mysql.connector
from mysql.connector import errorcode
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse, redirect, render
from mysite.mysite.search import db_connection
import json
from datetime import datetime
import pytz


def feedback(request):
    return render(request, 'feedback.html')


def sendfeedback(request):
    conn = db_connection()
    feedback = request.POST
    way = feedback.get('select2')
    mycursor = conn.MysqlDB.cursor()
    tz = pytz.timezone("Asia/Shanghai")
    time = datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO `feedback` (`Message`,`{}`,`type`,`create_time`) VALUES (%s,%s,%s,%s)".format(way)
    val = (feedback.get('message'), feedback.get('value'), feedback.get('select1'), time)
    mycursor.execute(sql, val)
    conn.MysqlDB.commit()
    mycursor.close()
    conn.close()
    return render(request, 'feedback_end.html')
