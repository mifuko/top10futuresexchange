import pandas as pd
import matplotlib.pyplot as plt
import shutil
import time
import zipfile
from time import sleep
import pandas as pd
import numpy as np
import csv
import os
import re
import glob



wmonth = '06'
wday = '16'

# with open(r'D:\origin_dce\0616\20230616_m2405_成交量_买持仓_卖持仓排名.txt', 'r', encoding='utf-8') as file:
# 遍历文件夹内所有 txt 文件


in_folder = 'D:/origin_dce/0616/'
out_folder = 'D:/origin_dce/0616/'
replace_col_num_1 = 3  # 这里使用你想要的列索引值
replace_col_num_2 = 5  # 这里使用你想要的列索引值
replace_col_num_3 = 4  # 这里使用你想要的列索引值
replace_col_num_4 = 6  # 这里使用你想要的列索引值
out_file = r'D:/origin_dce/0616/merged.csv'


for filename in os.listdir(in_folder):
    if filename.endswith('.txt'):
        # 读取原始文件
        file_path = os.path.join(in_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as txtfile:
            lines = txtfile.readlines()

        # 删除前7行
        lines = lines[6:]

        # 将指定列中的千分位逗号去掉 成交量 3 增减量 5 replace_col_num = 3
        for i, line in enumerate(lines):
            cols = line.split('\t')
            if len(cols) > replace_col_num_1:
                cols[replace_col_num_1] = cols[replace_col_num_1].replace(',', '')
                lines[i] = '\t'.join(cols)

        for i, line in enumerate(lines):
            cols = line.split('\t')
            if len(cols) > replace_col_num_2:
                cols[replace_col_num_2] = cols[replace_col_num_2].replace(',', '')
                lines[i] = '\t'.join(cols)

        for i, line in enumerate(lines):
            cols = line.split('\t')
            if len(cols) > replace_col_num_3:
                cols[replace_col_num_3] = cols[replace_col_num_3].replace(',', '')
                lines[i] = '\t'.join(cols)

        for i, line in enumerate(lines):
            cols = line.split('\t')
            if len(cols) > replace_col_num_4:
                cols[replace_col_num_4] = cols[replace_col_num_4].replace(',', '')
                lines[i] = '\t'.join(cols)


        # 写入修正后文件
        with open(file_path, 'w', encoding='utf-8') as txtfile:
            txtfile.write(''.join(lines))


"""
file_list = [
    r'D:/origin_dce/0616/20230616_a2307_成交量_买持仓_卖持仓排名.txt',
    r'D:/origin_dce/0616/20230616_a2309_成交量_买持仓_卖持仓排名.txt',
    r'D:/origin_dce/0616/20230616_a2311_成交量_买持仓_卖持仓排名.txt']  # 按照需要的顺序排列文件

with open(out_file, 'w', encoding='utf-8') as outfile:
    for filename in file_list:
        file_path = os.path.join(in_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            outfile.write(content)

"""


with open(out_file, 'w', encoding='utf-8') as outfile:
    for filename in os.listdir(in_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(in_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()
                sleep(0.5)
                outfile.write(content)


# "C:\Users\kidor\Downloads\20230616_DCE_DPL.zip"
# shutil.move('C:/Users/kidor/Downloads/2023'+wmonth+wday+'_DCE_DPL.zip', 'D:/origin_dce/dceqh'+wmonth+wday+'.zip')

brokerlist = ['东证期货', '中信期货', '海通期货', '华泰期货', '国泰君安', '方正中期',
              '永安期货', '五矿期货', '南华期货', '金瑞期货', '浙商期货', '光大期货',
              '银河期货', '广发期货', '国信期货', '国投安信', '国联期货', '东方财富',
              '中辉期货', '宝城期货', '财信期货', '齐盛期货', '国富期货', '华闻期货',
              '中泰期货', '金瑞期货', '兴证期货', '中金财富']








# combpath = 'D:/origin_dce/' + wmonth + wday + '/comb.csv'
# combined_df = pd.concat(df_list)
# combined_df.to_csv(os.path.join(folder_path, combpath), index=False)

# 读取csv文件，将成交量列解析为数字类型
# data = pd.read_csv(combpath, usecols=[2, 3], thousands=',', header=1)
# data = data.dropna()
# data['成交量'] = pd.to_numeric(data['成交量'], errors='coerce')
# data.to_csv('D:/origin_dce/datatest.csv', index=False)
