import json
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import time
import pymysql
from django.core.paginator import Paginator, Page  # 翻頁
from django.db import connection, connections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import math
import pymysql.cursors
from myapp.models import News, Class as study, IndexClass
from django.db import connection as conn
from pymysql import cursors
from myapp import trade_frame


# ----




from pymysql import cursors
from urllib.parse import unquote
from myapp.mods import futuresDateTime as fdt
from myapp.mods.bt_frame import Strategy
from myapp.mods.bt_frame_algo import Strategy_algo, GenericCSVData_Predict
from myapp.mods.bt_dataframe import bt_dataframe, bt_result_dataframe
import backtrader as bt
import pandas as pd
# 載入指定檔案路徑相關的模組
import os
from pathlib import Path
import datetime
from pandas import Period
# 改----
from rest_framework.views import APIView
from rest_framework import viewsets
from myapp.mods import futuresDateTime as fdt
from django.http import JsonResponse
from Facade import TechnicalIndicatorsImgFacade
from myapp.models import Soy, Tx, Mtx, Te, Tf, MiniDow, MiniNastaq, MiniSp, MiniRussell, ADebt, Wheat, Corn,TechnicalStrategry,Member
# -----

# 連線至資料庫
db_settings = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "futurewarbler",
    "charset": "utf8",
    "cursorclass": pymysql.cursors.DictCursor
}
conn = pymysql.connect(**db_settings)

# Create your views here.


def index(request):
    news3 = News.objects.all()[:5]
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
        return render(request, "index.html", {'News': news3, 'ok': ok, 'username': username, 'photo': photo})
    else:
        ok = ''
        username = ''
        photo = ''
        return render(request, "index.html", {'News': news3, 'ok': ok, 'username': username, 'photo': photo})
# --------------登出----------------------


def logout(request):

    if request.method == 'POST':
        if request.POST['logout'] == "logout":
            request.session.flush()
    return redirect('/index/')
# --------------登入功能------------------


def login(request):
    if 'username' in request.session:
        return redirect('/index/')  # 如果處於登入狀態，只要人為方式回到login，就會自動跳轉到index
    if request.method == 'POST':
        account = request.POST['account']
        password = request.POST['password']
        cursor = connection.cursor()

        sql = "SELECT * FROM `member` WHERE `member_id` ='%s'" % (account)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data == None:  # 這個帳號沒人註冊
            message = '此帳號尚未註冊，請再次確認'
        else:
            if password != data[1]:  # 帳號密碼錯誤
                message = '帳號密碼錯誤，請再次確認'
            else:
                request.session['userid'] = account
                request.session['password'] = password
                request.session['username'] = data[2]
                request.session['gender'] = data[3]
                request.session['birth'] = data[4].strftime(
                    "%Y-%m-%d")  # type=datetime.date
                request.session['photo'] = data[5]
                request.session['phone'] = data[6]
                request.session['mail'] = data[7]

                return redirect('/index/')
    return render(request, "login.html", locals())


# --------------註冊功能------------------
def register(request):
    if request.method == 'POST':
        account = request.POST['account']
        password = request.POST['password']
        photopath = request.FILES.get('photo', False)
        name = request.POST['name']
        gender = request.POST['gender']
        birth = request.POST['birth']
        phone = request.POST['phone']
        mail = request.POST['mail']
        if account == "" or password == "" or name == "" or photopath == False or gender == "" or birth == "" or phone == "" or mail == "":
            lostSomething = "lostSomething"
            checkLost = "您少填了部分資料請先再次檢查"
            return render(request, "register.html", locals())
        else:
            if gender == 0:
                sex = 'M'
            else:
                sex = 'F'
            with conn.cursor() as cursor:
                sql = "SELECT * FROM `member` WHERE `member_id` LIKE ('%s')" % (
                    account)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    check = 'no'
                    message = '您輸入的帳戶有人使用，請重新輸入帳戶:'
                    return render(request, "register.html", locals())
                else:
                    # 照片上傳部分
                    photo = request.FILES['photo']
                    photoname = request.FILES['photo'].name
                    uploadphoto = account+'_'+photoname
                    with open('static/userimg/'+uploadphoto, 'wb+') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)
                    # -----------
                    sql = "INSERT INTO `member`(`member_id`, `member_password`, `member_name`, `member_photo`, `member_gender`, `member_birth`, `member_phone`, `member_email`) VALUES ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s')" % (
                        account, password, name, uploadphoto, sex, birth, phone, mail)
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
                    request.session['username'] = account
                    request.session['photo'] = uploadphoto
                    photo = request.session['photo']
                    username = request.session['username']
                    return render(request, 'index.html', locals())

    return render(request, "register.html", locals())
# ------------未登入狀態下的個人頁面-----------------


def personal_unlogin(request):
    if 'username' in request.session:
        return redirect('/personal/')
    return render(request, "personal-page(unlogin).html", locals())

# ------------登入狀態下的個人頁面-----------------


def personal(request):

    if 'username' in request.session:
        ok = "yes"
        userid = request.session['userid']
        username = request.session['username']
        photo = request.session['photo']
        userid = request.session['userid']
        gender = request.session['gender']
        phone = request.session['phone']
        mail = request.session['mail']
        if gender == 'F':
            gender = '女'
        else:
            gender = '男'
        phone = request.session['phone']
        mail = request.session['mail']
        birth = request.session['birth']
    else:
        return redirect('/personal-unlogin/')

    return render(request, "personal-page.html", locals())

# ------------個人介面個人資料修改--------------------


def update(request):
    account = request.session['userid']
    cursor = connection.cursor()
    if request.method == 'POST':

        if request.POST['update'] == 'password':  # 表示要修密碼
            if request.POST['password'] == request.POST['password2']:

                message = '個人資料修改完成!^^'
                password = request.POST['password']
                password2 = request.POST['password2']
                sql = "UPDATE `member` SET `member_password`='%s' WHERE `member_id` ='%s'" % (
                    password, account)
                cursor.execute(sql)

            else:

                message = '兩個密碼不一樣啦!'
                return redirect('/personal/', alertmessage=message)

        else:  # 表示要修其他個人資訊

            if 'username' in request.POST:
                username = request.POST['username']
                request.session['usrname'] = username

            if 'gender' in request.POST:
                gender = request.POST['gender']
                request.session['gender'] = gender

            photopath = request.FILES.get('photo', False)
            if photopath == False:
                photo = request.session['photo']
            else:
                photo = request.FILES['photo']
                photoname = request.session['photo']  # 因為要蓋掉之前的照片，所以名子要一樣
                with open('static/userimg/'+photoname, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)
                request.session['photo'] = photoname

            # 因為birth是必填選項，所以不用判斷
            birth = request.POST['birth']

            if 'phone' in request.POST:
                phone = request.POST['phone']
                if len(phone) < 9:
                    phone = request.session['phone']
                else:
                    phone = request.POST['phone']

            if 'mail' in request.POST:
                mail = request.session['mail']
                request.session['mail'] = mail

            mail = request.session['mail']
            username = request.session['username']
            photo = request.session['photo']
            gender = request.session['gender']
            if gender == "0":
                gender = 'M'
            else:
                gender = 'F'

            sql = "UPDATE `member` SET `member_name`='%s', `member_gender`='%s',`member_birth`='%s',`member_photo`='%s',`member_phone`='%s',`member_email`='%s' WHERE `member_id` ='%s'" % (
                username, gender, birth, photo, phone, mail, account)
            try:

                message = "成功更改資料!>.-"
                cursor.execute(sql)

            except:

                message = "出錯嚕>.-"
                return redirect('/personal/', alertmessage=message)

    return redirect('/personal/', alertmessage=message)


# ------------個人介面交易紀錄-----------------------
def transactionRecord(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        return redirect('/personal-unlogin/')
    return render(request, "personal-transactionRecord.html", locals())


# ------------個人介面策略清單-----------------------
def strategy(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
        memberid = request.session['memberId']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
        # results = TechnicalStrategry.objects.filter(memberId=memberid)
        
        # for i in results :
        #     print(i)
    return redirect('/personal-unlogin/')
    
    # if request.method == 'POST':
    #     code = request.POST['code']
    #     strategyname = request.POST['strategyname']
    #     goodname = request.POST['goodname']
    #     amount = request.POST['amount']
    #     cycle = request.POST['cycle']
    #     starttime = request.POST['start-time']
    #     endtime = request.POST['end-time']
    #     bullbearchoice = request.POST['bullbearchoice']
    #     pin = request.POST['pin']
    #     out = request.POST['out']
    #     alname = request.POST['alname']
    #     monout = request.POST['monout']
    #     stopLoss = request.POST['stopLoss']
        
    #     print(stopLoss,code,cycle,bullbearchoice)
    #     results = TechnicalStrategry.objects.filter(class_title__contains=keyWord)
# def classes(request):
    
#     if 'keyWord' in request.GET:
#         keyWord = request.GET['keyWord']
#         #keyWord2 = '期貨'
#         keyWord = unquote(keyWord)
#         results = study.objects.filter(class_title__contains=keyWord)
        
#         return render(request, "class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})
#     if 'page' in request.GET:
#         try:
#             page = int(request.GET['page'])*6
#             # Class as study  # [page-6:page]代表一頁資料數量
#             results = study.objects.all()[page-6:page]
#             return render(request, "class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})
#         except:
#             results = study.objects.all()[:6]
#             return render(request, "class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})
#     else:
#         results = study.objects.all()[:6]
#         return render(request, "class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})

# -------------模擬交易所---------------------


def trade(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
        return redirect('/personal-unlogin/')
    TXData = Tx.objects.all().order_by("-tx_date")[:1]
    MTXData = Mtx.objects.all().order_by("-mtx_date")[:1]
    TEData = Te.objects.all().order_by("-te_date")[:1]
    TFData = Tf.objects.all().order_by("-tf_date")[:1]
    YMData = MiniDow.objects.all().order_by("-mini_dow_date")[:1]
    NQData = MiniNastaq.objects.all().order_by("-mini_nastaq_date")[:1]
    ESData = MiniSp.objects.all().order_by("-mini_sp_date")[:1]
    RTYData = MiniRussell.objects.all().order_by("-mini_russell_date")[:1]
    TYData = ADebt.objects.all().order_by("-a_debt_date")[:1]
    soyData = Soy.objects.all().order_by("-soy_date")[:1]
    wheatData = Wheat.objects.all().order_by("-wheat_date")[:1]
    cornData = Corn.objects.all().order_by("-corn_date")[:1]
    # for item in soy1[:1]:
    #     print(item.id)
    #     print("結束")
    return render(request, "trade.html", {"Tx": TXData, "Mtx": MTXData, "Te": TEData, "Tf": TFData, "MiniDow": YMData, "MiniNastaq": NQData, "MiniSp": ESData, "MiniRussell": RTYData, "ADebt": TYData, "Soy": soyData, "Wheat": wheatData, "Corn": cornData})


# -----------------策略交易機器人--------------------------
def robotnormal(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
        # 如果成功傳送策略包
        if 'strategy_pack' in request.session:
            # 把存在session中的策略包內容物全部用變數接出來
            strategy = request.session['strategy_pack']
            long_short = strategy["long_short"]  # 做空做多
            money_manage = strategy["money_manage"]  # 資金管理
            freq = strategy['period']  # 資料集時間週期
            start = strategy["start"]  # 資料集開始時間
            end = strategy["end"]  # 資料集結束時間
            enter = strategy["enter"]  # 進場策略
            exit = strategy["exit"]  # 出場策略
            futures = strategy["futures"]  # 期貨
            stop_pl = strategy['stop_pl'].split("/")  # 停損停利/停損範圍/停利範圍
            stop = stop_pl[0]  # 停損停利代號

            if stop_pl[0] == "point":  # 固定式
                stop_loss = float(stop_pl[1])
                stop_profit = float(stop_pl[2])

            elif stop_pl[0] == "percentage":  # 百分比
                stop_loss = float(stop_pl[1])
                stop_profit = float(stop_pl[2])
            else:  # 移動停損
                stop_loss = float(stop_pl[1])

            message = ("我們session是有東西的", futures, "停損:",
                       stop_loss, "資料開始時間:", start, stop_pl)

            """
               把回測功能寫在這邊
            """
            if futures == 'tx':
                margin = 18400
            elif futures == 'mtx':
                margin = 46000
            elif futures == 'te':
                margin = 180000
            elif futures == 'tf':
                margin = 79000
            elif futures == 'mini_dow':
                margin = 9350
            elif futures == 'mini_nasdaq':
                margin = 18700
            elif futures == 'mini_sp':
                margin = 12650
            elif futures == 'mini_russell':
                margin = 6600
            elif futures == 'soy':
                margin = 2915
            elif futures == 'wheat':
                margin = 2063
            elif futures == 'corn':
                margin = 1678

            # =========backtrader==================
            # 還沒接資料集

            cerebro = bt.Cerebro()
            cerebro.broker.setcash(10000000)
            cerebro.broker.setcommission(commission=0.001, margin=margin)
            value = cerebro.broker.getvalue()
            cerebro.addstrategy(Strategy, longshort=long_short, instrategy=enter, outstrategy=exit,stopstrategy=stop, losspoint=stop_loss, profitpoint=stop_profit, tmp=value, moneymanage=money_manage)
            # 載入資料集

            data_path = Path(os.getcwd())/'myapp\\mods\\MXF1-2年-1小時.csv'
            data = bt.feeds.GenericCSVData(dataname=data_path,
                                           fromdate=datetime.datetime(
                                               2019, 1, 1),
                                           todate=datetime.datetime(
                                               2019, 12, 31),
                                           nullvalue=0.0,
                                           dtformat=('%Y-%m-%d'),
                                           tmformat=('%H:%M:%S'),
                                           date=0,
                                           time=1,
                                           high=3,
                                           low=4,
                                           open=2,
                                           close=5,
                                           volume=6,
                                           openinterest=-1)

            '''
            dataframe = fdt.futuresDateTime(futures, start, end, freq)
            data = bt.feeds.PandasData(dataname=dataframe,datetime=None, open=0, close=1, low=2, high=3, volume=4, openinterest=None)
            '''
            cerebro.adddata(data)
            # 抓最初資產
            start_value = cerebro.broker.getvalue()
            # 加入績效分析
            cerebro.addanalyzer(bt.analyzers.AnnualReturn,
                                _name='AnnualReturn')
            cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
            cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SR')
            cerebro.addanalyzer(bt.analyzers.Returns, _name='RS')
            cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')
            cerebro.addanalyzer(bt.analyzers.TradeAnalyzer,
                                _name='TradeAnalyzer')

            cerebro.run(runonce=False)
            cerebro.plot()
            results = cerebro.run()
            start = results[0]
            # 抓最終資產
            end_value = cerebro.broker.getvalue()
            """
            print("Final Portfolio {}".format(cerebro.broker.getvalue()))
            print('收益:{:,.2f}'.format(end_value-start_value))
            print('年利潤:', start.analyzers.AnnualReturn.get_analysis())
            print('最大策略虧損:', start.analyzers.DW.get_analysis()["max"]["drawdown"])
            print('夏普指數:', start.analyzers.SR.get_analysis()["sharperatio"])
            print('總收益率:', start.analyzers.RS.get_analysis()["rtot"])
            """
            finalPortfolio = cerebro.broker.getvalue()
            earning = end_value-start_value
            overallYield = start.analyzers.RS.get_analysis()["rtot"]
            MDD = start.analyzers.DW.get_analysis()["max"]["drawdown"]
            sharpeRatio = start.analyzers.SR.get_analysis()["sharperatio"]
            SQN = start.analyzers.SQN.get_analysis()["sqn"]
            earnLossRatio = start.analyzers.TradeAnalyzer.get_analysis()[
                'won']['pnl']['average'] / (-1 * start.analyzers.TradeAnalyzer.get_analysis()['lost']['pnl']['average'])
            profitFactor = start.analyzers.TradeAnalyzer.get_analysis()[
                'won']['pnl']['total'] / (-1 * start.analyzers.TradeAnalyzer.get_analysis()['lost']['pnl']['total'])
            transactionsCount = start.analyzers.TradeAnalyzer.get_analysis()[
                'total']['total']
            profitCount = start.analyzers.TradeAnalyzer.get_analysis()[
                'won']['total']
            lossCount = start.analyzers.TradeAnalyzer.get_analysis()[
                'lost']['total']
            winRate = start.analyzers.TradeAnalyzer.get_analysis(
            )['won']['total'] / start.analyzers.TradeAnalyzer.get_analysis()['total']['total']
            # =========backtrader==================
            # 先把策略包備份到看不到的地方
            request.session['strategy_pack_backup'] = strategy
            del request.session['strategy_pack']  # 刪除回測用策略包，以免每次近來都要先回測一次降低效能
        else:
            message = "沒東西"
    else:
        return redirect('/personal-unlogin/')
    return render(request, "robot-normal.html", locals())

# ----------------策略機器人傳送至資料庫---------------------


def send_strategy_sql(request):
    member_id = request.session['userid']
    strategy = request.session['strategy_pack_backup']
    strategy_name = request.POST['strategy_name']
    stop_pl = strategy['stop_pl']
    long_short = strategy["long_short"]  # 做空做多
    money_manage = strategy["money_manage"]  # 資金管理
    period = strategy["period"]  # 資料集時間週期
    start = strategy["start"]  # 資料集開始時間
    end = strategy["end"]  # 資料集結束時間
    enter = strategy["enter"]  # 進場策略
    exit = strategy["exit"]  # 出場策略
    futures = strategy["futures"]  # 期貨商品

    with conn.cursor() as cursor:
        sql = "INSERT INTO `technical_strategry`(`technical_strategry_period`, `technical_strategry_start`, `technical_strategry_end`, `technical_strategry_enter`, `technical_strategry_exit`, `futures_id`, `member_id`, `technical_strategy_long_short`, `technical_strategy_stop_pl`, `technical_strategy_money_manage`, `technical_strategy_id`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            period, start, end, enter, exit, futures, member_id, long_short, stop_pl, money_manage, strategy_name)
        cursor.execute(sql)
        conn.commit()

    return redirect('/robot-normal/')

# -----------------智能交易機器人--------------------------


def robotintelligent(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
        # 如果成功傳送策略包
        if 'ai_strategy_pack' in request.session:
            # 把存在session中的策略包內容物全部用變數接出來
            ai_strategy = request.session['ai_strategy_pack']
            ai_long_short = ai_strategy["long_short"]  # 做空做多
            ai_money_manage = ai_strategy["money_manage"]  # 資金管理
            ai_algorithm = ai_strategy["algorithm"]  # 演算法
            ai_futures = ai_strategy["futures"]  # 期貨
            ai_stop_pl = ai_strategy['stop_pl'].split("/")  # 停損停利/停損範圍/停利範圍
            ai_stop = ai_stop_pl[0]  # 停損停利代號
            if ai_stop_pl[0] == "point":  # 固定式
                ai_stop_loss = float(ai_stop_pl[1])
                ai_stop_profit = float(ai_stop_pl[2])

            elif ai_stop_pl[0] == "percentage":  # 百分比
                ai_stop_loss = float(ai_stop_pl[1])
                ai_stop_profit = float(ai_stop_pl[2])
            else:  # 移動停損
                ai_stop_loss = float(ai_stop_pl[1])

            message = ("我們session是有東西的", ai_futures, ai_money_manage,
                       ai_algorithm, ai_stop_pl, ai_stop_loss, ai_stop_profit)
            """
            演算法窗個顯示
            """
            resultFilename = bt_result_dataframe(
                ai_futures, ai_long_short, ai_algorithm)
            result_df = pd.read_csv(resultFilename)

            # 讀取 accuracy
            accuracy_0, accuracy_1, accuracy_2, accuracy_3, accuracy_4, accuracy_5, accuracy_6, accuracy_7, accuracy_8, accuracy_9, accuracy_10, accuracy_11, accuracy_12, accuracy_13, accuracy_14, accuracy_15, accuracy_16, accuracy_17, accuracy_average, accuracy_dev = result_df['accuracy'][0], result_df['accuracy'][1], result_df['accuracy'][2], result_df['accuracy'][3], result_df['accuracy'][4], result_df['accuracy'][5], result_df['accuracy'][6], result_df['accuracy'][7], result_df['accuracy'][8], result_df[
                'accuracy'][9], result_df['accuracy'][10], result_df['accuracy'][11], result_df['accuracy'][12], result_df['accuracy'][13], result_df['accuracy'][14], result_df['accuracy'][15], result_df[
                'accuracy'][16], result_df['accuracy'][17], result_df['accuracy'][18], result_df['accuracy'][19]

            # 讀取 f1-score
            f1_0, f1_1, f1_2, f1_3, f1_4, f1_5, f1_6, f1_7, f1_8, f1_9, f1_10, f1_11, f1_12, f1_13, f1_14, f1_15, f1_16, f1_17, f1_average, f1_dev = result_df['f1_macro'][0], result_df['f1_macro'][1], result_df['f1_macro'][2], result_df['f1_macro'][3], result_df['f1_macro'][4], result_df['f1_macro'][5], result_df['f1_macro'][6], result_df['f1_macro'][7], result_df['f1_macro'][8], result_df[
                'f1_macro'][9], result_df['f1_macro'][10], result_df['f1_macro'][11], result_df['f1_macro'][12], result_df['f1_macro'][13], result_df['f1_macro'][14], result_df['f1_macro'][15], result_df[
                'f1_macro'][16], result_df['f1_macro'][17], result_df['f1_macro'][18], result_df['f1_macro'][19]

            """
               把回測功能寫在這邊
            """
            if ai_futures == 'tx':
                margin = 18400
            elif ai_futures == 'mtx':
                margin = 46000
            elif ai_futures == 'te':
                margin = 180000
            elif ai_futures == 'tf':
                margin = 79000
            elif ai_futures == 'mini_dow':
                margin = 9350
            elif ai_futures == 'mini_nasdaq':
                margin = 18700
            elif ai_futures == 'mini_sp':
                margin = 12650
            elif ai_futures == 'mini_russell':
                margin = 6600
            elif ai_futures == 'soy':
                margin = 2915
            elif ai_futures == 'wheat':
                margin = 2063
            elif ai_futures == 'corn':
                margin = 1678

            cerebro = bt.Cerebro()
            cerebro.broker.setcash(10000000)
            # 券商保證金以及手續費設定
            cerebro.broker.setcommission(commission=0.001, margin=margin)
            value = cerebro.broker.getvalue()

            cerebro.addstrategy(Strategy_algo, longshort=ai_long_short, algostrategy=ai_algorithm,
                                stopstrategy=ai_stop, losspoint=ai_stop_loss, profitpoint=ai_stop_profit, tmp=value, moneymanage=ai_money_manage)
            # 加入資料集 先用mtx並且先假裝做"多"
            filename = bt_dataframe(ai_futures, ai_long_short, ai_algorithm)
            # 載入資料集
            data = GenericCSVData_Predict(dataname=filename,
                                          fromdate=datetime.datetime(
                                              2018, 1, 1),
                                          todate=datetime.datetime(2020, 1, 1),
                                          nullvalue=0.0,
                                          dtformat=('%Y-%m-%d'),
                                          tmformat=('%H:%M:%S'),
                                          date=0,
                                          time=1,
                                          high=3,
                                          low=5,
                                          open=2,
                                          close=4,
                                          volume=6,
                                          predict=7,
                                          openinterest=-1)

            cerebro.adddata(data)
            # 抓最初資產
            start_value = cerebro.broker.getvalue()
            # 加入績效分析
            cerebro.addanalyzer(bt.analyzers.AnnualReturn,
                                _name='AnnualReturn')
            cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
            cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SR')
            cerebro.addanalyzer(bt.analyzers.Returns, _name='RS')
            cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')
            cerebro.addanalyzer(bt.analyzers.TradeAnalyzer,
                                _name='TradeAnalyzer')
            #print("start profolio {}".format(cerebro.broker.getvalue()))
            cerebro.run(runonce=False)
            #print("final profolio {}".format(cerebro.broker.getvalue()))

            results = cerebro.run()
            start = results[0]
            # 抓最終資產
            end_value = cerebro.broker.getvalue()
            """
            print("Final Portfolio {}".format(cerebro.broker.getvalue()))
            print('收益:{:,.2f}'.format(end_value-start_value))
            print('年利潤:', start.analyzers.AnnualReturn.get_analysis())
            print('最大策略虧損:', start.analyzers.DW.get_analysis()["max"]["drawdown"])
            print('夏普指數:', start.analyzers.SR.get_analysis()["sharperatio"])
            print('總收益率:', start.analyzers.RS.get_analysis()["rtot"])
            """
            finalPortfolio = cerebro.broker.getvalue()
            earning = end_value-start_value
            overallYield = start.analyzers.RS.get_analysis()["rtot"]
            MDD = start.analyzers.DW.get_analysis()["max"]["drawdown"]
            sharpeRatio = start.analyzers.SR.get_analysis()["sharperatio"]
            SQN = start.analyzers.SQN.get_analysis()["sqn"]
            """
            earnLossRatio = start.analyzers.TradeAnalyzer.get_analysis()['won']['pnl']['average'] / (-1 * start.analyzers.TradeAnalyzer.get_analysis()['lost']['pnl']['average'])
            profitFactor = start.analyzers.TradeAnalyzer.get_analysis()['won']['pnl']['total'] / (-1 * start.analyzers.TradeAnalyzer.get_analysis()['lost']['pnl']['total'])
            transactionsCount = start.analyzers.TradeAnalyzer.get_analysis()['total']['total']
            profitCount = start.analyzers.TradeAnalyzer.get_analysis()['won']['total']
            lossCount = start.analyzers.TradeAnalyzer.get_analysis()['lost']['total']
            winRate = start.analyzers.TradeAnalyzer.get_analysis()['won']['total'] / start.analyzers.TradeAnalyzer.get_analysis()['total']['total']

            """

            # 先把策略包備份到看不到的地方
            request.session['ai_strategy_pack_backup'] = ai_strategy
            # 刪除回測用策略包，以免每次近來都要先回測一次降低效能
            del request.session['ai_strategy_pack']
        else:
            message = "沒東西"
    else:
        return redirect('/personal-unlogin/')
    return render(request, "robot-intelligent.html", locals())


# ----------------智能機器人傳送至資料庫---------------------

def send_ai_strategy_sql(request):
    member_id = request.session['userid']
    ai_strategy = request.session['ai_strategy_pack_backup']
    ai_strategy_name = request.POST['ai_strategy_name']
    ai_strategy_algorithm = ai_strategy["algorithm"]
    ai_stop_pl = ai_strategy["stop_pl"]
    ai_long_short = ai_strategy["long_short"]  # 做空做多
    ai_money_manage = ai_strategy["money_manage"]  # 資金管理
    ai_futures = ai_strategy["futures"]  # 期貨商品

    with conn.cursor() as cursor:
        sql = "INSERT INTO `intelligent_strategy`(`intelligent_strategy_id`, `futures_id`, `member_id`, `intelligent_strategy_long_short`, `intelligent_strategy_algorithm`, `intelligent_strategy_money_manage`, `intelligent_strategy_stop_pl`) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
            ai_strategy_name, ai_futures, member_id, ai_long_short, ai_strategy_algorithm, ai_money_manage, ai_stop_pl)
        cursor.execute(sql)
        conn.commit()
        conn.close()

    return redirect('/robot-intelligent/')

# -------------------期貨小教室----------------------------


def classes(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
    if 'keyWord' in request.GET:
        keyWord = request.GET['keyWord']
        #keyWord2 = '期貨'
        keyWord = unquote(keyWord)
        results = study.objects.filter(class_title__contains=keyWord)

        return render(request, "class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})
    if 'page' in request.GET:
        try:
            page = int(request.GET['page'])*6
            # Class as study  # [page-6:page]代表一頁資料數量
            results = study.objects.all()[page-6:page]
            return render(request, "class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})
        except:
            results = study.objects.all()[:6]
            return render(request, "class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})
    else:
        results = study.objects.all()[:6]
        return render(request, "class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})


def classcontent(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
    pk = request.GET["id"]
    cursor = conn.cursor()
    cursor.execute(
        "select class_id,class_title,class_article,class_photo from class where class_id=%s" % (pk))
    class1 = study.objects.filter(pk=pk)
    class1 = cursor.fetchall()
    return render(request, "class-content.html", {'Class1': class1, 'ok': ok, 'username': username, 'photo': photo})


def indexclass(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
    if 'page' in request.GET:
        try:
            page = int(request.GET['page'])*6
            # [page-6:page]代表一頁資料數量
            results = IndexClass.objects.all()[page-6:page]
            return render(request, "index-class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})
        except:
            results = IndexClass.objects.all()[:6]
            return render(request, "index-class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})
    else:
        results = IndexClass.objects.all()[:6]
        return render(request, "index-class.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo})


def indexclasscontent(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
    pk = request.GET["id"]
    cursor = conn.cursor()
    cursor.execute(
        "select index_class_id,index_class_title,index_class_article,index_class_photo from index_class where index_class_id=%s" % (pk))
    indexclass1 = IndexClass.objects.filter(pk=pk)
    indexclass1 = cursor.fetchall()
    return render(request, "index-class-content.html", {'Indexclass1': indexclass1, 'ok': ok, 'username': username, 'photo': photo})


def news(request):
    # new2 最新 news3熱門
    # 如果html 裡 category=category ，判斷是category 0 財經 1 期貨 2 兩岸 3  國際 4產業 5理財
    # news3裡 抓category 裡的type最新與熱門
    # 如果try 裡抓page一頁有幾個，下一頁
    # except 防止報錯
    # else 防止報錯
    # print(request.GET['page'])
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
    if 'category' in request.GET:
        category = int(request.GET['category'])
        news3 = News.objects.filter(
            news_category=category).filter(news_type=1)[:4]
        titleWord = {
            "0": "財經總覽",
            "1": "期貨相關",
            "2": "兩岸財經",
            "3": "國際財經"
        }
        title = titleWord[str(category)]
        if 'page' in request.GET:
            try:
                page = int(request.GET['page'])*5
                news2 = News.objects.all()[page-4:page]
                return render(request, "news-1.html", {'News2': news2, 'News3': news3, "title": title, "category": str(category), 'ok': ok, 'username': username, 'photo': photo})
            except:
                page = request.GET['page']
                news2 = News.objects.all()[:5]
                return render(request, "news-1.html", {'News2': news2, 'News3': news3, "title": title, "category": str(category), 'ok': ok, 'username': username, 'photo': photo})
        else:
            category = int(request.GET['category'])
            news2 = News.objects.filter(
                news_category=category).filter(news_type=0)[:5]
            news3 = News.objects.filter(
                news_category=category).filter(news_type=1)[:5]
            return render(request, "news-1.html", {'News2': news2, 'News3': news3, "title": title, "category": str(category), 'ok': ok, 'username': username, 'photo': photo})
    else:

        category = int(request.GET['category'])
        news3 = News.objects.all()[:5]
        news2 = News.objects.all()[:5]
        return render(request, "news-1.html", {'News2': news2, 'News3': news3, "category": str(category), 'ok': ok, 'username': username, 'photo': photo})


def newscontent(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
    pk = request.GET["id"]
    cursor0 = connection.cursor()
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()
    cursor4 = connection.cursor()
    cursor5 = connection.cursor()
    cursor6 = connection.cursor()
    cursor7 = connection.cursor()
    cursor8 = connection.cursor()
    cursor9 = connection.cursor()
    cursor10 = connection.cursor()
    cursor11 = connection.cursor()
    cursor12 = connection.cursor()
    cursor13 = connection.cursor()
    cursor14 = connection.cursor()
    cursor15 = connection.cursor()
    cursor16 = connection.cursor()
    cursor17 = connection.cursor()
    cursor18 = connection.cursor()
    cursor19 = connection.cursor()
    cursor20 = connection.cursor()
    cursor21 = connection.cursor()
    cursor22 = connection.cursor()

    cursor0.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['0'])
    cursor1.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['1'])
    cursor2.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['2'])
    cursor3.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['3'])
    cursor4.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['4'])
    cursor5.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['5'])
    cursor6.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['6'])
    cursor7.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['7'])
    cursor8.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['8'])
    cursor9.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['9'])
    cursor10.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['10'])
    cursor11.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['11'])
    cursor12.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor13.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor14.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor15.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor16.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor17.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor18.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor19.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor20.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor21.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))
    cursor22.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_id=%s" % (pk))

    news1 = News.objects.filter(pk=pk)
    news2 = News.objects.filter(pk=pk)
    news3 = News.objects.filter(pk=pk)
    news4 = News.objects.filter(pk=pk)
    news5 = News.objects.filter(pk=pk)
    news6 = News.objects.filter(pk=pk)
    news7 = News.objects.filter(pk=pk)
    news8 = News.objects.filter(pk=pk)
    news9 = News.objects.filter(pk=pk)
    news10 = News.objects.filter(pk=pk)
    news11 = News.objects.filter(pk=pk)
    news12 = News.objects.filter(pk=pk)
    news13 = News.objects.filter(pk=pk)
    news14 = News.objects.filter(pk=pk)
    news15 = News.objects.filter(pk=pk)
    news16 = News.objects.filter(pk=pk)
    news17 = News.objects.filter(pk=pk)
    news18 = News.objects.filter(pk=pk)
    news19 = News.objects.filter(pk=pk)
    news20 = News.objects.filter(pk=pk)
    news21 = News.objects.filter(pk=pk)

    news0 = cursor0.fetchall()[:5]
    news1 = cursor1.fetchall()[:5]
    news2 = cursor2.fetchall()[:5]
    news3 = cursor3.fetchall()[:5]
    news4 = cursor4.fetchall()[:5]
    news5 = cursor5.fetchall()[:5]
    news6 = cursor6.fetchall()[:5]
    news7 = cursor7.fetchall()[:5]
    news8 = cursor8.fetchall()[:5]
    news9 = cursor9.fetchall()[:5]
    news10 = cursor10.fetchall()
    news11 = cursor11.fetchall()
    news12 = cursor12.fetchall()
    news13 = cursor13.fetchall()
    news14 = cursor14.fetchall()
    news15 = cursor15.fetchall()
    news16 = cursor16.fetchall()
    news17 = cursor17.fetchall()
    news18 = cursor18.fetchall()
    news19 = cursor19.fetchall()
    news20 = cursor20.fetchall()
    news21 = cursor21.fetchall()

    return render(request, "news-content.html", {'News0': news0, 'News1': news1, 'News2': news2, 'News3': news3, 'News4': news4, 'News5': news5, 'News6': news6, 'News7': news7, 'News8': news8, 'News9': news9, 'News10': news10, 'News11': news11, 'News12': news12, 'News13': news13, 'News14': news14, 'News15': news15, 'News16': news16, 'News17': news17, 'News18': news18, 'News19': news19, 'News20': news20, 'News21': news21, 'ok': ok, 'username': username, 'photo': photo})


def news1(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
    cursor2 = conn.cursor()
    cursor2.execute(
        "select news_id,news_title,news_time,news_author,news_photo,news_content,news_area from news where news_area=%s", ['2'])
    news2 = cursor2.fetchall()[:5]
    # 期貨
    return render(request, "index.html", {'News2': news2, 'ok': ok, 'username': username, 'photo': photo})


def newssearch(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        ok = ''
        username = 'no'
        photo = 'no'
    if 'keyWord' in request.GET:
        keyWord = request.GET['keyWord']
        #keyWord2 = '期貨'
        keyWord = unquote(keyWord)
        # results = News.objects.filter(news_title__contains=keyWord)
        if 'page' in request.GET:
            try:
                page = int(request.GET['page'])*6
                # Class as study  # [page-6:page]代表一頁資料數量
                results = News.objects.filter(
                    news_title__contains=keyWord)[page-6:page]
                return render(request, "news-search.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo, 'keyWord': keyWord})
            except:
                results = News.objects.filter(
                    news_title__contains=keyWord)[page-6:page]
                return render(request, "news-search.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo, 'keyWord': keyWord})
        else:
            results = News.objects.filter(news_title__contains=keyWord)[0:6]
            return render(request, "news-search.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo, 'keyWord': keyWord})

    # return render(request, "news-search.html", {'results': results, 'ok': ok, 'username': username, 'photo': photo,'keyWord':keyWord})

# -------------------未平倉契約頁面-------------------------


def contract(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        return redirect('/personal-unlogin/')
    return render(request, "contract.html", locals())


# ------------------我的訂單頁面---------------------------
def order(request):
    if 'username' in request.session:
        ok = 'yes'
        username = request.session['username']
        photo = request.session['photo']
    else:
        return redirect('/personal-unlogin/')
    return render(request, "order.html", locals())

# ------------策略清單測試-----------------------


def strategy_normal(request):
    if request.method == 'POST':
        product = request.POST['product']
        stop = request.POST['stop']
        long_short = request.POST['long_short']
        in_strategy = request.POST['in_strategy']
        out_strategy = request.POST['out_strategy']
        fix = request.POST['fix']
        account = request.session['userid']
        cycle_number = request.POST['cycle_number']
        cycle = request.POST['cycle']
        start = request.POST['start-time']
        end = request.POST['end-time']

        # 時間週期
        period = cycle_number + cycle

        if fix == "4":
            fix = "fix_lot"
        elif fix == "5":
            fix = "fix_money"
        else:
            fix = "fix_rate"

        if long_short == "0":
            long_short = "long"
            if in_strategy == '0':
                in_strategy = "long-in-ma"
            elif in_strategy == '1':
                in_strategy = "long-in-osc"
            elif in_strategy == '2':
                in_strategy = "long-in-rsi"
            elif in_strategy == '3':
                in_strategy = "long-in-kd"
            elif in_strategy == '4':
                in_strategy = "long-in-bias"
            else:
                in_strategy = "long-in-william"

            if out_strategy == "0":
                out_strategy = "long-out-ma"
            elif out_strategy == "1":
                out_strategy = "long-out-rsi"
            elif out_strategy == "2":
                out_strategy = "long-out-kd"
            elif out_strategy == "3":
                out_strategy = "long-out-bias"
            else:
                out_strategy = "long-out-william"
        else:
            long_short = "short"
            if in_strategy == '0':
                in_strategy = "short-in-ma"
            elif in_strategy == '1':
                in_strategy = "short-in-osc"
            elif in_strategy == '2':
                in_strategy = "short-in-rsi"
            elif in_strategy == '3':
                in_strategy = "short-in-kd"
            elif in_strategy == '4':
                in_strategy = "short-in-bias"
            else:
                in_strategy = "short-in-william"

            if out_strategy == "0":
                out_strategy = "short-out-ma"
            elif out_strategy == "1":
                out_strategy = "short-out-rsi"
            elif out_strategy == "2":
                out_strategy = "short-out-kd"
            elif out_strategy == "3":
                out_strategy = "short-out-bias"
            else:
                out_strategy = "short-out-william"

        if stop == "1":
            stop_name = "percentage"
            stop1 = request.POST['stop1-1']
            stop2 = request.POST['stop1-2']
            stop_name = stop_name+"/"+stop1+"/"+stop2
        elif stop == "2":
            stop_name = "point"
            stop1 = request.POST['stop2-1']
            stop2 = request.POST['stop2-2']
            stop_name = stop_name+"/"+stop1+"/"+stop2
        else:
            stop_name = "move"
            stop1 = request.POST['stop3']
            stop_name = stop_name+"/"+stop1

        strategy_pack = {
            "member_id": account,
            "long_short": long_short,
            "stop_pl": stop_name,
            "money_manage": fix,
            "period": period,
            "start": start,
            "end": end,
            "enter":  in_strategy,
            "exit": out_strategy,
            "futures": product,
        }
        request.session['strategy_pack'] = strategy_pack

    return redirect('/robot-normal/')


def test(request):
    strategy = request.session['strategy_pack_backup']
    futures = strategy['futures']
    start = strategy['start']
    end = strategy['end']
    freq = strategy['period']
    dataframe = fdt.futuresDateTime(futures, start, end, freq)

    return render(request, "test.html", locals())


# ------------智能策略清單測試-----------------------
def strategy_ai(request):
    if request.method == 'POST':
        product = request.POST['product']
        stop = request.POST['stop']
        long_short = request.POST['long_short']
        fix = request.POST['fix']
        account = request.session['userid']
        algorithm = request.POST['algorithm']

        # 演算法
        if algorithm == '1':
            algorithm = 'svm'
        elif algorithm == '2':
            algorithm = 'rf'
        elif algorithm == '3':
            algorithm = 'ada'
        else:
            algorithm = 'gep'

        # 資金管理
        if fix == "4":
            fix = "fix_lot"
        elif fix == "5":
            fix = "fix_money"
        else:
            fix = "fix_rate"
        # 多空
        if long_short == "0":
            long_short = "long"
        else:
            long_short = "short"

        # 停損停利
        if stop == "1":
            stop_name = "percentage"
            stop1 = request.POST['stop1-1']
            stop2 = request.POST['stop1-2']
            stop_name = stop_name+"/"+stop1+"/"+stop2
        elif stop == "2":
            stop_name = "point"
            stop1 = request.POST['stop2-1']
            stop2 = request.POST['stop2-2']
            stop_name = stop_name+"/"+stop1+"/"+stop2
        else:
            stop_name = "move"
            stop1 = request.POST['stop3']
            stop_name = stop_name+"/"+stop1

        ai_strategy_pack = {
            "member_id": account,
            "long_short": long_short,
            "stop_pl": stop_name,
            "algorithm": algorithm,
            "money_manage": fix,
            "futures": product,
        }
        request.session['ai_strategy_pack'] = ai_strategy_pack

    return redirect('/robot-intelligent/')

# ---------------- backtrader test --------------------------
def RobotNormalSample(request):
    return render(request,"RobotNormalSample.html",locals())
class GetTechnicalImgHeml(APIView): # 畫圖
    def post(self, request, *args, **kwargs):
        futures = request.data['data']['stock']
        freq = request.data['data']['timePeriod']
        startTime = request.data['data']['startTime']
        endTime = request.data['data']['endTime']
        lineOne = request.data['data']['lineOne']
        lineTwo = request.data['data']['lineTwo']
        print(futures,freq,startTime,endTime,lineOne,lineTwo)
        fileName  = futures
        doType = [lineOne,lineTwo]
        print(doType)
        chart_data = ""
        df = []
        technicalImgFacade = TechnicalIndicatorsImgFacade(fileName,doType,chart_data,df,startTime,endTime,futures,freq)
        # 859引用facade裡定義得直
        technicalImgFacade.chart_data = technicalImgFacade.get_data()
        technicalImgFacade.doType = doType
        hemlName = technicalImgFacade.draw_charts()
        ret = {'code': 200, 'msg': '成功',"hemlName" : hemlName}
        return JsonResponse(ret)
    
class GetTechnicalType(APIView):
    def get(self, request, *args, **kwargs):
        #TechnicalType = [{"TypeName":"MA"},{"TypeName":"RSI"},{"TypeName":"BIAS"},{"TypeName":"Real"},{"TypeName":"KD"},{"TypeName":"MACD"}]
        data = []
        TechnicalType = ["MA","RSI","BIAS","Real","KD","MACD"]
        #data = TechnicalType
        for i in TechnicalType:
            list = {
                "TypeName": i
            }
            data.append(list)
        ret = {'code': 200, 'msg': '成功',"data" : data}
        #print(ret)
        return JsonResponse(ret)
# 連的api
# class GetUserTransactionRecord(APIView):
#     def post(self, request, *args, **kwargs):
#         data = []
#         print(request.GET['memberId'])
#         futeresID = "Test"
#         futuresName = "Test"
#         record: "Test"
#         buy_qty: "Test"
#         buy_mon: "Test"
#         buy_time: "Test"
#         sell_qty: "Test"
#         sell_mon: "Test"
#         sell_time: "Test"
#         return_rate: "Test"
#         for i in range(0,5):
#             list = {
#                 "futeresID": i,
#                 "futuresName": i,
#                 "record": i,
#                 "buy_qty":i,
#                 "buy_mon": i,
#                 "buy_time": i,
#                 "sell_qty": i,
#                 "sell_mon": i,
#                 "sell_time": i,
#                 "return_rate": i
#             }
#         data.append(list)
#         ret = {'code': 200, 'msg': '成功',"data" : data}
#         return JsonResponse(ret)
class GetUserAccount(APIView):
    def post(self, request, *args, **kwargs):
        data = []
        print(request.GET['memberId'])
        member_twd = "Test"
        member_usd = "Test"
        for i in range(0,5):
            list = {
                "member_twd" :i,
                "member_usd" :i,
                "return_rate":i
            }
            data.append(list)
        ret = {'code': 200, 'msg': '成功',"data" : data}
        return JsonResponse(ret)
class UserRecordFree(APIView): 
    def __init__(self) -> None:
        self.useData = []
        self.ConfirmUseData
        
    def post(self, request, *args, **kwargs):
        
        stock = request.data['data']['stock']
        timePeriod = request.data['data']['timePeriod']
        startTime = request.data['data']['startTime']
        endTime = request.data['data']['endTime']
        longshort = request.data['data']['longshort']
        inst = request.data['data']['inst']
        outst = request.data['data']['outst']
        fix = request.data['data']['fix']
        loss = request.data['data']['loss']
        profit = request.data['data']['profit']
        
        print(stock,timePeriod,startTime,endTime,longshort,inst,outst,fix,loss,profit)
        if  self.ConfirmUseData() != True : 
            ret = {'code': 9999, 'msg': '運算失敗，缺少必要欄位',}
            print(ret)
            return JsonResponse(ret)
        else:
            print("開始")
            #丟進運算的方法
            # 商品名稱、時間、price
            setStrategy = trade_frame.SetStrategy()
            # 錢（從資料庫撈）
            setStrategy.cash = 500000
            # 最大買賣值
            setStrategy.maxQuan  = 10
            # delta 變數
            setStrategy.delta = 10000
            # 保證金（stock 查 enum）
            setStrategy.doData = stock
            path = "/Users/sally/FutureWarbler-Final/FutureWarbler/myapp/mods/"
            if setStrategy.doData =="tf":
                df = f"{path}/2017-2022-tf-1min.csv"
            elif setStrategy.doData =="te":
                df = f"{path}/2017-2022-te-1min.csv"
            elif setStrategy.doData =="tx":
                df =  f"{path}/2017-2022-tx-1min.csv"
            elif setStrategy.doData =="mtx":
                df = f"{path}/2017-2022-mtx-1min.csv"
            elif setStrategy.doData =="c":
                df = f"{path}/2017-2022-corn-1min.csv"
            elif setStrategy.doData =="nas":
                df = f"{path}/2017-2022-E-mini-nasdaq-1min.csv" 
            elif setStrategy.doData =="rut":
                df = f"{path}/2017-2022-E-mini-russell-1min.csv"
            elif setStrategy.doData =="sp":
                df = f"{path}/2017-2022-E-mini-s&p-1min.csv"
            elif setStrategy.doData =="udf" :
                df = f"{path}/2017-2022-mini_dow_1min.csv"
            elif setStrategy.doData =="s" :
                df = f"{path}/2017-2022-soybean-1min.csv"
            elif setStrategy.doData =="w":
                df = f"{path}/2017-2022-wheat-1min.csv"
            else:
                df = f"{path}/2017-2022-a_debt-1min.csv"
            # 商品列表（stock 查 ）
            setStrategy.useData = df
            setStrategy.longshort = int(longshort)
            setStrategy.instrategy = int(inst)
            setStrategy.outstrategy = int(outst)
            setStrategy.profit = int(profit)
            setStrategy.loss = int(loss)
            setStrategy.moneymanage = int(fix)
            print(setStrategy.useData)
            setStrategy.SetValue()
            ret = {'code': 200, 'msg': '成功'}
            print(ret)
            return JsonResponse(ret)

    def ConfirmUseData(self)-> bool:
        # for item in self.useData:
        #     if item == "" :
        #         return False
        #     else:    
        #         continue
        return True
        
class UserRecord(APIView): # 畫圖
    def post(self, request, *args, **kwargs):
        memberId = request.GET['memberId']
        strategry_name = request.GET['technical_strategry_name']
        if  memberId == "": 
            ret = {'code': 9999, 'msg': '運算失敗，缺少必要欄位',}
            print(ret)
            return JsonResponse(ret)
        else:
            #使用memberId查詢是否有此會員用ORM撈出來後面加這個方法exists()
            #News.objects.all().exists()
            #類似上面這種但要換成比對帳號
            #上面出來會是bool值
            if memberId == "" :
                ret = {'code': 9998, 'msg': '運算失敗，沒有此會員',}
                print(ret)
                return JsonResponse(ret)
            else:
                #取該會員所有的紀錄資料
                #丟進運算的方法
                userDate = TechnicalStrategry.objects.filter(member_id= memberId).filter(technical_strategry_name=strategry_name)
                for i in userDate:
                    print(i.technical_strategry_period)
                    print(i.technical_strategry_start)
                    print(i.technical_strategry_end)
                    print(i.technical_strategry_enter)
                    print(i.technical_strategry_exit)
                    print(i.technical_strategy_long_short)
                    print(i.technical_strategy_stop_pl)
                    print(i.technical_strategy_money_manage)
                setStrategy = trade_frame.SetStrategy()
                setStrategy.cash = 500000
                setStrategy.maxQuan  = 10
                setStrategy.delta = 10000
                setStrategy.doData = "P002" 
                setStrategy.useStrategy = 'FixedSizeStrategy'
                setStrategy.useData = '/Users/user/Downloads/FutureWarblerWeb-feature-ApiRecordAndRecharge/FutureWarblerWeb-feature-ApiRecordAndRecharge/myapp/backtrader_Data_test/MXF1-Minute-Trade(小台指分鐘-2016-1-1至2021--12-22).csv'
                setStrategy.SetValue()
                ret = {'code': 200, 'msg': '成功'}
                print(ret)
                return JsonResponse(ret)
    
class Recharge(APIView): # 畫圖
    def post(self, request, *args, **kwargs):
        memberId = request.GET['memberId']
        member_twd = request.GET['member_twd']
        member_usd = request.GET['member_usd']
        print(memberId)
        print(member_twd)
        print(member_usd)
        if  memberId == "" or (member_twd == "" and member_usd == "") : 
            ret = {'code': 9999, 'msg': '儲值失敗，缺少必要欄位',}
            print(ret)
            return JsonResponse(ret)
        else:
            if memberId == "" :
                ret = {'code': 9998, 'msg': '儲值失敗，沒有此會員',}
                print(ret)
                return JsonResponse(ret)
            else:
                memberdate = Member.objects.filter(member_id=memberId)
                for i in memberdate:
                    twd = i.member_twd + member_twd
                    usd = i.member_usd + member_usd
                Member.objects.filter(member_id=memberId).update(member_twd=twd,member_usd=usd)
                ret = {'code': 200, 'msg': '儲值成功',}
                print(ret)
                return JsonResponse(ret)
class GetTechnicalStrategry(APIView):
    def get(self, request, *args, **kwargs):
        memberId = request.GET['memberId']
        print(memberId)
        data = []
        memberTransa = TechnicalStrategry.objects.filter(member_id= memberId)
        
        for i in memberTransa:
            list = {
                "technical_strategry_name" :i.technical_strategry_name,
                "member" :memberId,
            }
            data.append(list)
        print(data)
        ret = {'code': 200, 'msg': '成功',"data" : data}
        return JsonResponse(ret)