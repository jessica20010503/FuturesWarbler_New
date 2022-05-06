from calendar import day_abbr
from cmath import nan
from ctypes import Array
from operator import index
import string
from time import time
import time as ti
from traceback import print_tb
from tracemalloc import start
from numpy import array
import requests
from typing import List, Union
import sys
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid
import csv
#import pandas as pd
from datetime import date, datetime
from . import IndicatorFacade as Indicator
# import futuresDateTime as fd
from myapp.mods import futuresDateTime as fdt
import pandas as pd


class TechnicalIndicatorsImgFacade:
    def __init__(self, fileName: str, doType, chart_data, df, start, end, futures, freq) -> None:
        self.fileName = fileName
        self.doType = []
        self.chart_data = chart_data
        self.df = []
        # 開始結束時間加入
        self.startTime = start
        self.end = end
        self.futures = futures
        self.freq = freq
        pass
    # 整理資料

    def split_data(self):
        category_data = []
        values = []
        volumes = []
        # print(self.df)
        # time.sleep(60)
        for i, tick in enumerate(self.df):
            # print(tick)
            # print(i)
            # time.sleep(60)
            category_data.append(tick[0])
            values.append(tick)
            volumes.append([i, tick[4], 1 if tick[1] > tick[2] else -1])
        # print(category_data)
        # print(values)
        # print(volumes)
        # time.sleep(60)
        return {"categoryData": category_data, "values": values, "volumes": volumes}

    # 範例MA
    def calculate_ma(self, day_count: int, data):
        # print(data)
        # print("進入MA")
        result: List[Union[float, str]] = []
        for i in range(len(data["values"])):
            # print(i)
            if i < day_count:
                # print('未知')
                result.append("-")
                continue
            sum_total = 0.0
            for j in range(day_count):
                # print(sum_total)
                sum_total += float(data["values"][i - j][1])

            result.append(abs(float("%.3f" % (sum_total / day_count))))
        # print(result)
        return result

    # 整合指標
    def TechnicalIndicators(self, day_count: int, data, doType):
        if doType == "MA":
            result = self.calculate_ma(day_count=5, data=data)
            return result
        # 要設定過往時間
        Date = "20160102"
        result: List[Union[float, str]] = []
        KBar = Indicator.KBar(Date, 'time', 1)
        df = data
        # 進場判斷
        Index = 0
        # 預設趨勢為1，假設只有多單進場
        Trend = 1
        for i in range(len(data["values"])):
            # time = datetime.datetime.strptime(data["values"][i][0],'%Y/%m/%d %H:%M:%S')
            time = datetime.strptime(data["values"][i][0], '%Y-%m-%d %H:%M:%S')
            price = float(data["values"][i][1])
            qty = float(data["values"][i][5])
            tag = KBar.TimeAdd(time, price, qty)

            # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
            if tag != 1:
                continue
            if doType == "RSI":
                RSIPeriod = 12
                FastPeriod = 5
                SlowPeriod = 15
                result = KBar.GetRSI(RSIPeriod)
            elif doType == "BIAS":
                # print("BIAS")
                BIASPeriod = 10
                Positive = 0.001
                Negative = -0.001
                result = KBar.GetBIAS(BIASPeriod)
            elif doType == "Real":
                WILLRPeriod = 14
                OverBuy = -20
                OverSell = -80
                result = KBar.GetWILLR(WILLRPeriod)
            elif doType == "KD":
                K, D = KBar.GetKD()
                result = {
                    "K": K,
                    "D": D
                }
                result['K']
            elif doType == "MACD":
                FastPeriod = 12
                SlowPeriod = 24
                MACDPeriod = 7
                DIF, MACD, OSC = KBar.GetMACD(
                    FastPeriod, SlowPeriod, MACDPeriod)
                result = {
                    "DIF": DIF,
                    "MACD": MACD
                }
        return result

    # 畫線數值
    def CreatLineDate(self, doType):
        if doType == "KD":
            kdDate = self.TechnicalIndicators(
                day_count=5, data=self.chart_data, doType=doType)
            line = (
                Line()
                .add_xaxis(xaxis_data=self.chart_data["categoryData"])
                .add_yaxis(
                    series_name="K",
                    # UseMA #K線快線（紅）
                    y_axis=kdDate["K"],
                    is_smooth=True,
                    is_hover_animation=False,
                    linestyle_opts=opts.LineStyleOpts(
                        width=3, opacity=0.5, color="#BF3434"),
                    label_opts=opts.LabelOpts(is_show=False),
                )
                .add_yaxis(
                    series_name="D",
                    # UseMA #D線慢線（藍）
                    y_axis=kdDate["D"],
                    is_smooth=True,
                    is_hover_animation=False,
                    linestyle_opts=opts.LineStyleOpts(
                        width=3, opacity=0.5, color="#262626"),
                    label_opts=opts.LabelOpts(is_show=False),
                )
            )
            return line

        elif doType == "MACD":
            MacdDate = self.TechnicalIndicators(
                day_count=5, data=self.chart_data, doType=doType)
            line = (
                Line()
                .add_xaxis(xaxis_data=self.chart_data["categoryData"])
                .add_yaxis(
                    series_name="DIF",
                    # UseMA #DIF快線（紅）
                    y_axis=MacdDate["DIF"],
                    is_smooth=True,
                    is_hover_animation=False,
                    linestyle_opts=opts.LineStyleOpts(
                        width=3, opacity=0.5, color="#63A6A6"),
                    label_opts=opts.LabelOpts(is_show=False),
                )
                .add_yaxis(
                    series_name="MACD",
                    # UseMA #MACD慢線（藍）
                    y_axis=MacdDate["MACD"],
                    is_smooth=True,
                    is_hover_animation=False,
                    linestyle_opts=opts.LineStyleOpts(
                        width=3, opacity=0.5, color="#D97E6A"),
                    label_opts=opts.LabelOpts(is_show=False),
                )
            )
            return line
        else:
            line = (
                Line()
                .add_xaxis(xaxis_data=self.chart_data["categoryData"])
                .add_yaxis(
                    series_name=doType,
                    # UseMA
                    y_axis=self.TechnicalIndicators(
                        day_count=5, data=self.chart_data, doType=doType),
                    is_smooth=True,
                    is_hover_animation=False,
                    linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
                    label_opts=opts.LabelOpts(is_show=False),
                )
            )
            return line

    # 畫線動作
    def draw_charts(self):
        # print(self.doType)
        # print(self.chart_data["values"])
        # time.sleep(60)
        kline_data = [data[1:-1] for data in self.chart_data["values"]]
        # 設定K線圖

        kline = (
            Kline()
            .add_xaxis(xaxis_data=self.chart_data["categoryData"])
            .add_yaxis(
                series_name="Dow-Jones index",
                y_axis=kline_data,
                itemstyle_opts=opts.ItemStyleOpts(
                    color="#ec0000", color0="#00da3c"),
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(
                    is_show=False, pos_bottom=10, pos_left="center"
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False,
                        type_="inside",
                        xaxis_index=[0, 1, 2],
                        range_start=98,
                        range_end=100,
                    ),
                    opts.DataZoomOpts(
                        is_show=True,
                        xaxis_index=[0, 1, 2],
                        type_="slider",
                        pos_top="85%",
                        range_start=98,
                        range_end=100,
                    ),
                    opts.DataZoomOpts(
                        is_show=True,
                        xaxis_index=[0, 1, 2],
                        type_="slider",
                        pos_top="85%",
                        range_start=98,
                        range_end=100,
                    ),
                ],
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    axis_pointer_type="cross",
                    background_color="rgba(245, 245, 245, 0.8)",
                    border_width=1,
                    border_color="#ccc",
                    textstyle_opts=opts.TextStyleOpts(color="#000"),
                ),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=False,
                    dimension=2,
                    series_index=5,
                    is_piecewise=True,
                    pieces=[
                        {"value": 1, "color": "#00da3c"},
                        {"value": -1, "color": "#ec0000"},
                    ],
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True,
                    link=[{"xAxisIndex": "all"}],
                    label=opts.LabelOpts(background_color="#777"),
                ),
                brush_opts=opts.BrushOpts(
                    x_axis_index="all",
                    brush_link="all",
                    out_of_brush={"colorAlpha": 0.1},
                    brush_type="lineX",
                ),
            )
        )
        # 設定第一個線圖
        line = self.CreatLineDate(self.doType[0])
        # 設定第二個線圖
        lineTwo = self.CreatLineDate(self.doType[1])

        # 宣告圖像大小
        grid_chart = Grid(
            init_opts=opts.InitOpts(
                width="1200px",
                height="1000px",
                animation_opts=opts.AnimationOpts(animation=False),
            )
        )
        # 宣告K線位置
        grid_chart.add(
            kline,
            grid_opts=opts.GridOpts(
                pos_left="6%", pos_right="8%", height="20%"),
        )
        # 宣告線圖1
        grid_chart.add(
            line,
            grid_opts=opts.GridOpts(
                pos_left="6%", pos_right="8%", pos_top="33%", height="10%"
            )
        )
        # 宣告線圖2
        grid_chart.add(
            lineTwo,
            grid_opts=opts.GridOpts(
                pos_left="6%", pos_right="8%", pos_top="48%", height="10%"
            ),
        )
        localtime = ti.localtime()
        nowTime = ti.strftime("%Y%m%d%H%M%S", localtime)
        # 生成heml到現在目錄下
        grid_chart.render(f"./static/ResultHtml/{nowTime}.html")
        return nowTime

    def get_data(self):

        # 計算週期
        print(self.futures)
        print(self.startTime)
        print(self.end)
        print(self.freq)
        path = "myapp\\mods"

        if self.futures == "tf":
            df = pd.read_csv(f"{path}\\2017-2021-tf-1min.csv")
        elif self.futures == "te":
            df = pd.read_csv(f"{path}\\2017-2022-te-1min.csv")
        elif self.futures == "tx":
            df = pd.read_csv(f"{path}\\2017-2022-tx-1min.csv")
        elif self.futures == "mtx":
            df = pd.read_csv(f"{path}\\2017-2022-mtx-1min.csv")
        elif self.futures == "corn":
            df = pd.read_csv(f"{path}\\2017-2022-corn-1min.csv")
        elif self.futures == "mini_nasdaq":
            df = pd.read_csv(f"{path}\\2017-2022-E-mini-nasdaq-1min.csv")
        elif self.futures == "mini_russell":
            df = pd.read_csv(f"{path}\\2017-2022-E-mini-russell-1min.csv")
        elif self.futures == "mini_sp":
            df = pd.read_csv(f"{path}\\2017-2022-E-mini-s&p-1min.csv")
        elif self.futures == "mini_dow":
            df = pd.read_csv(f"{path}\\2017-2022-mini_dow_1min.csv")
        elif self.futures == "soybean":
            df = pd.read_csv(f"{path}\\2017-2022-soybean-1min.csv")
        elif self.futures == "wheat":
            df = pd.read_csv(f"{path}\\2017-2022-wheat-1min.csv")
     
        df['DateTime'] = pd.to_datetime(
            df[self.futures+'_date'] + df[self.futures+'_time'], format='%Y-%m-%d%H:%M:%S')
        df[self.futures+'_date'] = pd.to_datetime(df[self.futures+'_date'])
        df[self.futures+'_time'] = pd.to_datetime(df[self.futures+'_time'])
        mask = (df[self.futures+'_date'] >=
                self.startTime) & (df[self.futures+'_date'] <= self.end)
        filtered_df = df.loc[mask]
        filtered_df = filtered_df.set_index("DateTime")
        df_final = filtered_df.groupby(pd.Grouper(freq=self.freq)).agg({
            # self.mtx_time"\:"DateTime",
            self.futures+"_date": "first",
            self.futures+"_time": "first",
            self.futures+"_open": "first",
            self.futures+"_high": "max",
            self.futures+"_low": "min",
            self.futures+"_close": "last",
            self.futures+"_volume": "sum"
        })
        df_final = df_final.dropna()
        # print(df_final)
# ------------------------------
        for item in df_final.values:
            data = []
            timeWord = str(item[0])[:10]+str(item[1])[10:]
            time = str(datetime.strptime(timeWord, "%Y-%m-%d %H:%M:%S"))
            print(timeWord)
            print(time)
            # data.append([time,item[2],item[3],item[4],item[5],item[6]])
            # print(data)
            # time.sleep(60)
            self.df.append([time, item[2], item[3], item[4], item[5], item[6]])
        # print(self.df)
        Data = self.split_data()
        print(Data)
        # time.sleep(60)
        return Data
