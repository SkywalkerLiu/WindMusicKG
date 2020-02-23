from mysite.mysite.settings import *
import mysql.connector
from mysql.connector import errorcode
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse, redirect, render
import json


class db_connection(object):
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


def db_query_school_by_id(id):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute("SELECT * from `school` where id = '{}'".format(id))
    results = mycursor.fetchall()
    if len(results) == 0:
        return None
    res = results[0]
    column_names = [i[0] for i in mycursor.description]
    final_result = dict()
    for i, column in enumerate(column_names):
        final_result[column] = res[i]
    mycursor.close()
    conn.close()
    return final_result


def db_query_company_by_id(id):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute("SELECT * from `company` where id = '{}'".format(id))
    results = mycursor.fetchall()
    if len(results) == 0:
        return None
    res = results[0]
    column_names = [i[0] for i in mycursor.description]
    final_result = dict()
    for i, column in enumerate(column_names):
        final_result[column] = res[i]
    mycursor.close()
    conn.close()
    return final_result


def db_query_school_for_singer_by_id(id):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute("SELECT * from `singer` where school_id = '{}'".format(id))
    results = mycursor.fetchall()
    if len(results) == 0:
        return None
    column_names = [i[0] for i in mycursor.description]
    final_results = []
    for res in results:
        temp = dict()
        for i, column in enumerate(column_names):
            if column == 'school_id' and res[i]:
                school_id = res[i]
                school_Info = db_query_school_by_id(school_id)
                temp['school'] = school_Info['name']
            elif column == 'company_id' and res[i]:
                company_id = res[i]
                company_Info = db_query_company_by_id(company_id)
                temp['company'] = company_Info['name']
            temp[column] = res[i]
        final_results.append(temp)
    mycursor.close()
    conn.close()
    return final_results


def db_query_company_for_singer_by_id(id):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute("SELECT * from `singer` where company_id = '{}'".format(id))
    results = mycursor.fetchall()
    if len(results) == 0:
        return None
    column_names = [i[0] for i in mycursor.description]
    final_results = []
    for res in results:
        temp = dict()
        for i, column in enumerate(column_names):
            if column == 'company_id' and res[i]:
                company_id = res[i]
                company_Info = db_query_company_by_id(company_id)
                temp['company'] = company_Info['name']
            elif column == 'company_id' and res[i]:
                company_id = res[i]
                company_Info = db_query_company_by_id(company_id)
                temp['company'] = company_Info['name']
            temp[column] = res[i]
        final_results.append(temp)
    mycursor.close()
    conn.close()
    return final_results


def db_query_singer_by_id(id):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute("SELECT * from `singer` where id = '{}'".format(id))
    results = mycursor.fetchall()
    if len(results) == 0:
        return None
    res = results[0]
    column_names = [i[0] for i in mycursor.description]
    final_result = dict()
    for i, column in enumerate(column_names):
        if column == 'school_id' and res[i]:
            school_id = res[i]
            school_Info = db_query_school_by_id(school_id)
            final_result['school'] = school_Info['name']
        elif column == 'company_id' and res[i]:
            company_id = res[i]
            company_Info = db_query_company_by_id(company_id)
            final_result['company'] = company_Info['name']
        final_result[column] = res[i]
    mycursor.close()
    conn.close()
    return final_result


def db_query_singer_name(name, similar=False):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    if similar:
        mycursor.execute("SELECT * from `singer` where baike_name like '%{}%'".format(name))
    else:
        mycursor.execute("SELECT * from `singer` where baike_name = '{}'".format(name))
    results = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]
    final_results = []
    for res in results:
        temp = dict()
        for i, column in enumerate(column_names):
            if column == 'school_id' and res[i]:
                school_id = res[i]
                school_info = db_query_school_by_id(school_id)
                school_name = school_info['name']
                temp['school'] = school_name
            elif column == 'company_id' and res[i]:
                company_id = res[i]
                company_info = db_query_company_by_id(company_id)
                company_name = company_info['name']
                temp['company'] = company_name
            temp[column] = res[i]
        final_results.append(temp)
    mycursor.close()
    conn.close()
    return final_results


def db_query_company_name(name, similar=False):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    if similar:
        mycursor.execute("SELECT * from `company` where `name` like '%{}%'".format(name))
    else:
        mycursor.execute("SELECT * from `company` where `name` = '{}'".format(name))
    results = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]
    final_results = []
    for res in results:
        temp = dict()
        for i, column in enumerate(column_names):
            temp[column] = res[i]
        final_results.append(temp)
    mycursor.close()
    conn.close()
    return final_results


def db_query_school_name(name, similar=False):
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    if similar:
        mycursor.execute("SELECT * from `school` where `name` like '%{}%'".format(name))
    else:
        mycursor.execute("SELECT * from `school` where `name` = '{}'".format(name))
    results = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]
    final_results = []
    for res in results:
        temp = dict()
        for i, column in enumerate(column_names):
            temp[column] = res[i]
        final_results.append(temp)
    mycursor.close()
    conn.close()
    return final_results


def query_singer(name, request):
    results = db_query_singer_name(name)
    show_columns = ('id', 'chinese_name', 'baike_url', 'birthdate', 'birthplace')
    show_columns_chinese = ('ID', '中文名', '出生日期', '出生地')
    if len(results) == 1:
        singer = results[0]
        return render(request, 'singer.html', {'singer': json.dumps(singer, ensure_ascii=False)})
    elif len(results) > 1:
        singers = []
        for result in results:
            temp = dict()
            for i in result:
                if i in show_columns: temp[i] = result[i]
            singers.append(temp)
        return render(request, 'confirm.html', {'singers': singers,'columns':show_columns_chinese})
    else:
        results = db_query_singer_name(name, similar=True)
        singers = []
        if len(results) > 0:
            for result in results:
                temp = dict()
                for i in result:
                    if i in show_columns:
                        temp[i] = result[i]
                singers.append(temp)
            return render(request, 'confirm.html', {'singers': singers,'columns':show_columns_chinese})
        else:
            return render(request, 'home.html', {'msg': '歌手不存在', 'feedback': True})


def query_school(name, request):
    show_columns = ('id','chinese_name','school','baike_url', 'birthdate', 'birthplace')
    show_columns_chinese = ('ID', '中文名', '毕业院校','出生日期', '出生地')
    results = db_query_school_name(name,similar=True)
    singer_results = []

    for res in results:
        singer_results += db_query_school_for_singer_by_id(res['id'])
    singers = []
    if len(singer_results) > 0:
        for result in singer_results:
            temp = dict()
            for i in result:
                if i in show_columns: temp[i] = result[i]
            singers.append(temp)
        return render(request, 'confirm.html', {'singers': singers, 'columns': show_columns_chinese})
    else:
        return render(request, 'home.html', {'msg': '找不到相关信息', 'feedback': True})


def query_company(name, request):
    show_columns = ('id', 'chinese_name', 'company', 'baike_url', 'birthdate', 'birthplace')
    show_columns_chinese = ('ID', '中文名', '出生日期', '出生地','经纪公司')
    results = db_query_company_name(name, similar=True)
    singer_results = []

    for res in results:
        singer_results += db_query_company_for_singer_by_id(res['id'])
    singers = []
    if len(singer_results) > 0:
        for result in singer_results:
            temp = dict()
            for i in result:
                if i in show_columns: temp[i] = result[i]
            singers.append(temp)
        return render(request, 'confirm.html', {'singers': singers, 'columns': show_columns_chinese})
    else:
        return render(request, 'home.html', {'msg': '找不到相关信息', 'feedback': True})


def query_singer_by_id(id, request):
    singer = db_query_singer_by_id(id)
    if singer:
        return render(request, 'singer.html', {'singer': json.dumps(singer, ensure_ascii=False)})
    else:
        return HttpResponse('ID不存在!')


def query(request):
    if request.method == 'GET':
        if request.GET.get('type') == 'singer':
            id = request.GET.get('id')
            if id is None:
                return redirect('/')
            else:
                return query_singer_by_id(id, request)
        else:
            return redirect('/')
    elif request.method == 'POST':
        if request.POST.get('type') == 'singer':
            name = request.POST.get('name')
            if name is None or name == '':
                return redirect('/')
            else:
                return query_singer(name, request)
        elif request.POST.get('type') == 'company':
            name = request.POST.get('name')
            if name is None or name == '':
                return redirect('/')
            else:
                return query_company(name, request)

        elif request.POST.get('type') == 'school':
            name = request.POST.get('name')
            if name is None or name == '':
                return redirect('/')
            else:
                return query_school(name, request)

        elif request.POST.get('type') == 'area':
            place = request.POST.get('name')
            if place is None:
                return redirect('/')
            else:
                return query_place(place, request)
        else:
            return redirect('/')
    else:
        return redirect('/')


def query_place(place, request):
    show_columns_chinese = ('ID', '中文名', '出生日期', '出生地')
    conn = db_connection()
    mycursor = conn.MysqlDB.cursor()
    mycursor.execute(
        "SELECT `id`,`chinese_name`,`birthdate`,`birthplace`,`baike_url` from `singer` where birthplace like '%{}%'".format(
            place))
    results = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]
    if len(results) >= 1:
        singers = []
        for res in results:
            singer = dict()
            for i, column in enumerate(column_names):
                singer[column] = res[i]
            singers.append(singer)
        conn.close()
        return render(request, 'confirm.html', {'singers': singers, 'columns': show_columns_chinese})
    else:
        return render(request, 'home.html', {'msg': '找不到相关信息', 'feedback': True})
