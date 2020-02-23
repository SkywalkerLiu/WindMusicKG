from mysite.mysite.settings import *
import mysql.connector
from mysql.connector import errorcode
from django.urls import path
from django.shortcuts import HttpResponse, redirect, render
import json
from Echarts_Experiments.mysite.mysite.search import db_connection
from datetime import datetime
import pytz


def admin(request):
    return render(request, 'adminHome.html')


def feedback(request):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute("SELECT * from `feedback` ORDER BY `create_time`")
    rows = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]
    results = []
    temp = dict()
    for row in rows:
        temp = dict()
        for i, column in enumerate(column_names):
            temp[column] = row[i]
        results.append(temp)
    mycursor.close()
    conn.close()
    return render(request, 'view_feedback.html', {'rows': results})
    pass


def singer(request):
    return render(request, 'adminSinger.html')
    pass


def insert_singer(singer):
    tz = pytz.timezone("Asia/Shanghai")
    current_time = datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO `singer` (`create_time`,`update_time`,"
    sql_s = "%s,%s,"
    val = [current_time,current_time]
    for key in singer:
        if singer[key] != '':
            sql += key + ','
            sql_s += '%s,'
            val.append(singer[key])
    if sql[-1] == ',':
        sql = sql[:-1]
    if sql_s[-1] == ',':
        sql_s = sql_s[:-1] + ')'
    # sql += ') VALUES (' + ('%s,' * (n - 1)) + '%s) '
    sql += ') VALUES (' + sql_s
    val = tuple(val)
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute(sql, val)
    conn.MysqlDB.commit()
    mycursor.close()
    conn.close()


def company(request):
    return HttpResponse('该功能暂未开放，敬请期待!')


def school(request):
    return HttpResponse('该功能暂未开放，敬请期待!')


def add_singer(request):
    chinese_to_english = {
        '百科名': 'baike_name',
        '中文名': 'chinese_name',
        '英文名': 'english_name', '别名': 'alias_name',
        '国籍': 'nationality', '祖籍': 'ancestral_home',
        '民族': 'nation', '星座': 'constellation',
        '血型': 'blood_type', '身高': 'height',
        '体重': 'weight', '出生地': 'birthplace',
        '出生日期': 'birthdate', '职业': 'career',
        '学校ID': 'school_id', '公司ID': 'company_id'}
    english_to_chines = {
        'baike_name': '百科名',
        'chinese_name': '中文名',
        'english_name': '英文名',
        'alias_name': '别名',
        'nationality': '国籍',
        'ancestral_home': '祖籍',
        'nation': '民族',
        'constellation': '星座',
        'blood_type': '血型',
        'height': '身高',
        'weight': '体重',
        'birthplace': '出生地',
        'birthdate': '出生日期',
        'career': '职业',
        'school_id': '学校ID', 'company_id': '经纪公司ID'}

    if request.method == 'GET':
        return render(request, 'addSinger.html', {'names': chinese_to_english})
    elif request.method == 'POST':
        info = request.POST
        if info.get('confirmed') == 'confirmed':
            try:
                singer = dict()
                for i in info:
                    if i not in ('_encoding', '_mutable', 'encoding', 'confirmed', '__len__'):
                        singer[i] = info[i]
                insert_singer(singer)
                return HttpResponse("添加歌手成功")
            except mysql.connector.Error as err:
                print(err.msg)
                return HttpResponse("添加歌手失败")
        else:
            singer = {i: info[i] for i in info}
            return render(request, 'add_confirm.html', {'singer': singer})
    else:
        return redirect('/')
