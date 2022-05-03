"""FutureWarbler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import index, login, register, personal, classes, classcontent, indexclass, indexclasscontent, robotnormal, robotintelligent, news, news1, newscontent, newssearch, trade, transactionRecord, strategy, logout, personal_unlogin, update, contract, order, strategy_normal, send_strategy_sql, test, strategy_ai, send_ai_strategy_sql
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('index/', index),
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
    path('personal/', personal),
    path('personal-unlogin/', personal_unlogin),
    path('transactionRecord/', transactionRecord),
    path('class/', classes),
    path('class-content/', classcontent),
    path('index-class/', indexclass),
    path('index-class-content/', indexclasscontent),
    path('robot-normal/', robotnormal),
    path('robot-intelligent/', robotintelligent),
    path('news/', news),
    path('news1/', news1),
    path('news-content/', newscontent),
    path('news-search/', newssearch),
    path('trade/', trade),
    path('strategy/', strategy),
    path('update/', update),
    path('contract/', contract),
    path('order/', order),
    path('strategy_normal/', strategy_normal),
    path('send_strategy_sql/', send_strategy_sql),
    path('test/', test),
    path('strategy_ai/', strategy_ai),
    path('send_ai_strategy_sql/', send_ai_strategy_sql),
    path('api/Recharge', views.Recharge.as_view()),
    path('api/GetUserAccount', views.GetUserAccount.as_view()),
    path('api/GetTechnicalStrategry', views.GetTechnicalStrategry.as_view()),
    path('api/GetTechnicalImgHeml', views.GetTechnicalImgHeml.as_view()),
    path('api/GetTechnicalType', views.GetTechnicalType.as_view()),
    path('api/UserRecord', views.UserRecord.as_view()),
    path('api/UserRecordFree', views.UserRecordFree.as_view()),
]
