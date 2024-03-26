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
out_file = r'D:/origin_dce/0616/merged.csv'
tmp_file = r'D:/origin_dce/0616/tmp.csv'
"""
with open(out_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for idx, rows in enumerate(reader):
        # 处理每一行数据
        for row in rows:
            # 使用制表符 '\t' 分隔字符串
            values = row.split('\t')
            #print(row)
            with open(tmp_file, 'a', encoding='utf-8') as ff:
                ff.write(row + '\n')
"""

brokerlist = ['东证期货', '中信期货', '海通期货', '华泰期货', '国泰君安', '方正中期',
              '永安期货', '五矿期货', '南华期货', '金瑞期货', '浙商期货', '光大期货',
              '银河期货', '广发期货', '国信期货', '国投安信', '国联期货', '东方财富',
              '中辉期货', '宝城期货', '财信期货', '齐盛期货', '国富期货', '华闻期货',
              '中泰期货', '金瑞期货', '兴证期货', '中金财富']


#data = pd.read_csv(tmp_file, header=0)
#data = data.rename(columns=lambda x: x.replace("'","").replace('"','')).replace(" ","")


#df_clean = pd.DataFrame(columns=['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5', 'Column 6', 'Column 7', 'Column 8'])

sleep(2)
df_csv = pd.read_csv(out_file, encoding='utf-8', delimiter="\t", sep='\t', error_bad_lines=False)
column_names = df_csv.columns.tolist()
#print(column_names)
#['名次', 'Unnamed: 1', '会员简称', '成交量', 'Unnamed: 4', '增减', 'Unnamed: 6', 'Unnamed: 7']
df_csv = df_csv.iloc[:, 2:4]
df_csv['成交量'] = pd.to_numeric(df_csv['成交量'], errors='coerce')

#print(df_csv.head(5))

# 定义一个字典，用于记录每个经纪人的交易额
broker_sum = {}

# 对于属于经纪人名单中的第一列数据，对应的第二列数值相加
for index, row in df_csv.iterrows():
    if row[0] in brokerlist:
        # 将字符串转换为浮点数或整数
        value = float(row[1])  # 或者 int(row[1])
        # 统计每个经纪人的交易额
        if row[0] not in broker_sum.keys():
            broker_sum[row[0]] = value
        else:
            broker_sum[row[0]] += value


df_csv = pd.DataFrame(list(broker_sum.items()), columns=['broker', 'sum'])
df_sorted = df_csv.sort_values('sum', ascending=False)
top_10 = df_sorted.head(10)

print(top_10)


# 绘制条形图并指定刻度格式和标签字体
ax = top_10.plot(kind='bar', x='broker', y='sum')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.1f}万'.format(x / 10000)))
ax.set_xticklabels(top_10['broker'])
ax.get_yaxis().set_label_coords(-0.1, 0.9)
plt.title('大商所'+wdate+'成交量前十的经纪商')
plt.show()




#new_column_names=['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5', 'Column 6', 'Column 7', 'Column 8']
#df_new = pd.DataFrame(df_csv['ColumnName'].str.split('\t', expand=True))
#df_new.columns = new_column_names


#print(df_new.head(5))














    # 使用 lambda 表达式处理每一行的数据
#    for row in reader:
        # 拆分行数据为多个列
#        columns = row[0].split(',')

        # 检查列数是否足够
#        if len(columns) < 8:
#            continue  # 如果列数不足，跳过该行数据
        # 处理拆分后的数据
#        col1, col2, col3, col4, col5, col6, col7, col8 = columns
        # 在这里编写你的处理代码
#        print(col1, col2, col3, col4, col5, col6, col7, col8)



# 将数据处理为 DataFrame 对象

# 查看 DataFrame 前五行
#print(data.columns)


# 打印出每列的属性
#print(data.dtypes)