import pymysql
import pandas as pd


table_name = '2021-05-03_2021-08-31'


_db = pymysql.connect(
    host="ls-a20f4420f7aa9967e25c1e0aecf4d8b641af5f13.cgtgapkuvqbt.ap-northeast-2.rds.amazonaws.com",
    db='1day_data',
    user = "dbmasteruser",
    password= "r,3Ipn|O7mL2vL4S)9Q~;7QVdHMV6R9j",
    port = 3306)


search_sql = f"SELECT * From `{table_name}`"

cursor = _db.cursor(pymysql.cursors.DictCursor)

cursor.execute(search_sql)            
result = cursor.fetchall() 

data_table = pd.DataFrame(result)

def final_list_():
    #'=30'에서 notnull인 df만들기
    asd = data_table[data_table['=30'].notnull()]
    date_list = asd['date'].tolist()
    code_list = asd['code'].tolist()
    final_list = []
    for i in zip(date_list, code_list):
        final_list.append(i)
    return final_list

final_list = final_list_()

print("="*60)
print(f'총 {len(final_list)}개 입니다!')
print("="*60)

final_list

######################################################################################################

ask_code = []

#레인지 안에는 완성된 깍두기 개수만큼 실행필요

for i in range(0,414):        
    lineEdit = final_list[i][1]
    exact_date = final_list[i][0]   
    ask_code.append(f'{lineEdit}_{exact_date}')

ask_code

######################################################################################################

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob
import argparse
import os
from shutil import copyfile, move
from pathlib import Path

# https://github.com/matplotlib/mpl_finance
# from mpl_finance import candlestick2_ochl, volume_overlay
from mplfinance.original_flavor import candlestick2_ochl, volume_overlay



def gold_egg(text_mod, dimension, use_volume, width_, width__, alpha_):
    print("Converting ohlc to candlestick")
    
    plt.style.use('dark_background')
    # text_mod.reset_index(inplace=True)
    text_mod['date'] = text_mod['date'].map(mdates.date2num) # 일봉일 경우 시간을 숫자로



    my_dpi = 300
    fig = plt.figure(figsize=(dimension / my_dpi, dimension / my_dpi), dpi=my_dpi)
    ax1 = fig.add_subplot(1, 1, 1)
    candlestick2_ochl(ax1, text_mod['open'], text_mod['close'], text_mod['high'],text_mod['low'],
                        width=width_,colorup='red', colordown='blue')
    ax1.grid(False)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_visible(False)
    ax1.axis('off')

    # create the second axis for the volume bar-plot
    # Add a seconds axis for the volume overlay
    if use_volume:
        ax2 = ax1.twinx()
        # Plot the volume overlay
        bc = volume_overlay(ax2, text_mod['open'], text_mod['close'], text_mod['volume'],
                            colorup='white', colordown='white', alpha=alpha_, width=width__)
        ax2.add_collection(bc)
        ax2.grid(False)
        ax2.set_xticklabels([])
        ax2.set_yticklabels([])
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        ax2.axis('off')

    plt.savefig(f'ac_{ask_code[i]}.png')
    plt.close(fig)

    # # Alpha 채널 없애기 위한.
    # from PIL import Image
    # img = Image.open(pngfile)
    # img = img.convert('RGB')
    # img.save(pngfile)

    print("Converting ohlc to candlestik finished.")

######################################################################################################

import pymysql
import pandas as pd
import re

#레인지 안에는 완성된 깍두기 개수만큼 실행필요

_db = pymysql.connect(
    host="ls-a20f4420f7aa9967e25c1e0aecf4d8b641af5f13.cgtgapkuvqbt.ap-northeast-2.rds.amazonaws.com",
    db='1day_upper_limit',
    user = "dbmasteruser",
    password= "r,3Ipn|O7mL2vL4S)9Q~;7QVdHMV6R9j",
    port = 3306)

try:
    # print(ask_code[1])
    for i ,j in enumerate(ask_code):
        # print(i)
        search_sql = f"SELECT * From `{j}`"

        cursor = _db.cursor(pymysql.cursors.DictCursor)

        cursor.execute(search_sql)            
        result = cursor.fetchall() 
        # print(result)
        # text_mod_1 = re.sub('^[0-9]{6}_[0-9]{4}-[0-9]{2}-[0-9]{2}',"***-****-****", i, flags=re.MULTILINE) 
        # print(text_mod)
        globals()[f'ac_{ask_code[i]}'] = pd.DataFrame(result)
        # print(ask_code[i])
        # print(globals())
        
except pymysql.ProgrammingError:
    pass   


######################################################################################################

# 데이터 조회 및 이미지 출력

for i in range(0,414):
    try:  
        pd.options.display.max_rows = 60
        text_mod = globals()[f'ac_{ask_code[i]}'].iloc[0:382:1,:]
        text_mod = text_mod.fillna(method='bfill')
        dimension = 3600
        use_volume = True

        gold_egg(text_mod, dimension, use_volume, 1, 1.5, 0.2)
        print(ask_code[i])

    except TypeError:
        pass
    except KeyError:
        pass
    except IndexError:
        pass

######################################################################################################