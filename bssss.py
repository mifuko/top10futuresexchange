#coding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


plt.rcParams['font.sans-serif'] = ['SimHei']

zceurl = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/2024/20240326/FutureDataTradeamt.htm"
zcepage = urllib.request.urlopen(zceurl)
soupzce = BeautifulSoup(zcepage)

#print(soupzce)

table = soupzce.find('table')
results = table.find_all('tr')

#print('number of res', len(results))
#print(results)

rows = []
rows.append(['名次','会员号','会员简称','成交量（手）','名次','会员号','会员简称','成交额（万元）'])
#print(rows)

for result in results:
    tddata = result.find_all('td')
    #print(tddata)

    if len(tddata) == 0:
        continue

    rank1 = tddata[0].getText()
    participateid1 = tddata[1].getText()
    participatename1 = tddata[2].getText()
    boardlot = tddata[3].getText()
    rank2 = tddata[4].getText()
    participateid2 = tddata[5].getText()
    participatename2 = tddata[6].getText()
    volume = tddata[7].getText()

    rows.append([rank1, participateid1, participatename1, boardlot, rank2, participateid2, participatename2, volume])


#print(rows)

with open('bbbs.csv', 'w', newline='', encoding='utf-8') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)

# 创建 brokerlist 列表
#brokerlist = ['中信期货', '东证期货', '海通期货', '国泰君安', '银河期货', '光大期货', '华泰期货', '华闻期货', '徽商期货',              '华西期货', '国信期货', '东吴期货', '中信建投', '广发期货', '渤海期货', '方正中期', '永安期货', '浙商期货','申银万国', '冠通期货']

# 读取 CSV 文件，并选择第 2 和第 9 列

# 读取 CSV 文件
df = pd.read_csv('bbbs.csv', usecols=[2, 3], header=1)


#print(df)

# 去除逗号分隔符，并将第二列数据转换为数字类型
df[df.columns[1]] = df[df.columns[1]].str.replace(',', '')
df[df.columns[1]] = pd.to_numeric(df[df.columns[1]])

#print(df)

top_10 = df.head(10)

print(top_10)

# 绘制条形图并指定刻度格式和标签字体
ax = top_10.plot(kind='bar', x='会员简称', y='成交量（手）')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.1f}万'.format(x / 10000)))
ax.set_xticklabels(top_10['会员简称'])
#ax.set_ylabel('成交量（万手）', fontweight='bold', rotation=90, labelpad=20)
ax.get_yaxis().set_label_coords(-0.1, 0.9)

# 显示图形
plt.show()