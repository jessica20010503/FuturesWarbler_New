
import requests as rq
from bs4 import BeautifulSoup
import time
import pandas as pd
import random
from datetime import datetime
import sys
import re

news_title = []
news_content = []
news_time = []
news_author= []
news_photo=[]
news_area = []
news_type = []
# type 0是最新 1熱門
news_category = []
# category 0 財經 1 期貨 2 兩岸 3  國際 4產業 5理財
df = pd.DataFrame()
#財經總覽最新
home_url = "https://money.udn.com/rank/newest/1001/0"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(0)
    news_type.append(0)
    news_category.append(0)
    time.sleep(1)
#財經總覽最熱
home_url = "https://money.udn.com/rank/pv/1001/0"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    # title_time = soup.select("div.item-content")[i].select("a")[1].text
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(1)
    news_type.append(1)
    news_category.append(0)
    time.sleep(1)
#最新期貨
home_url = "https://money.udn.com/rank/newest/1001/11111"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(2)
    news_type.append(0)    
    news_category.append(1)
    time.sleep(1)

#最熱門期貨
home_url = "https://money.udn.com/rank/pv/1001/11111"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(3)
    news_type.append(1)
    news_category.append(1)
    time.sleep(1)


#兩岸最新
home_url = "https://money.udn.com/rank/newest/1001/5589/1"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(4)
    news_type.append(0)
    news_category.append(2)
    time.sleep(1)
#兩岸最熱
home_url = "https://money.udn.com/rank/pv/1001/5589"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(5)
    news_type.append(1)
    news_category.append(2)
    time.sleep(1)
#國際最新
home_url = "https://money.udn.com/rank/newest/1001/5588"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(6)
    news_type.append(0)
    news_category.append(3)
    time.sleep(1)
#國際最熱
home_url = "https://money.udn.com/rank/pv/1001/5588"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(7)
    news_type.append(1) 
    news_category.append(3)
    time.sleep(1)

#產業最新
home_url = "https://money.udn.com/rank/newest/1001/5591"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(8)
    news_type.append(0)
    news_category.append(4)
    time.sleep(1)
#產業最熱
home_url = "https://money.udn.com/rank/pv/1001/5591"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(9)
    news_type.append(1)
    news_category.append(4)
    time.sleep(1)

#理財最新
home_url = "https://money.udn.com/rank/newest/1001/5592"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(10)
    news_type.append(0)
    news_category.append(5) 
    time.sleep(1)
#理財最熱
home_url = "https://money.udn.com/rank/pv/1001/5592"
r = rq.get(home_url)
soup = BeautifulSoup(r.text, "lxml")

for i in range(0, len(soup.select("div.story__content"))):
    url = soup.select("div.story__content")[i].select("a")[0]["href"]
    r_content =rq.get(url)
    soup_content = BeautifulSoup(r_content.text,"lxml")
    news_title.append("".join(x.text for x in soup_content.select("h1.article-head__title")))
    news_content.append("".join(x.text.replace('\n','').replace('\r','') for x in soup_content.select("section.article-body__editor p")))
    news_author.append("".join(x.text for x in soup_content.select("div.article-body__info span")))
    news_time.append(soup_content.find("time","article-body__time").text)
    news_photo.append(soup.select("div.story__image")[i].select("img")[0]["src"])
    news_area.append(11)
    news_type.append(1)
    news_category.append(5)
    time.sleep(1)
df["news_title"]=news_title  
df["news_content"]=news_content
df["news_time"]=news_time
df["news_author"]=news_author
df["news_photo"]=news_photo
df["news_area"]=news_area
df["news_type"]=news_type
df["news_category"]=news_category
from sqlalchemy import create_engine
conn = create_engine('mysql+pymysql://root:12345678@127.0.0.1:3306/futurewarbler?charset=utf8mb4')  
pd.io.sql.to_sql(df,'news',con=conn,if_exists='append')

