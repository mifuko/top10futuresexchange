#coding:utf-8
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 阶段排名

dceurl = "http://www.dce.com.cn/publicweb/quotesdata/memberDealCh.html"
dcepage = urllib.request.urlopen(dceurl)
soupdce = BeautifulSoup(dcepage)

#print(soupdce)

table = soupdce.find('table')
results = table.find_all('tr')

#print('number of res', len(results))
#print(results)

rows = []
rows.append(['名次','会员号','会员名称','成交量','成交量比重','名次','会员号','会员名称','成交额','成交额比重'])
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
    boardrate = tddata[4].getText()
    rank2 = tddata[5].getText()
    participateid2 = tddata[6].getText()
    participatename2 = tddata[7].getText()
    volume = tddata[8].getText()
    volumerate = tddata[9].getText()

    rows.append([rank1, participateid1, participatename1, boardlot, boardrate,rank2, participateid2, participatename2, volume, volumerate])

print(rows)

with open('dd.csv', 'w', newline='', encoding="utf-8") as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)


# 读取 CSV 文件
df = pd.read_csv('dd.csv', usecols=[2, 3, 4], header=1)
df = df.replace(r'\s', '', regex=True)

print(df)

# 去除逗号分隔符，并将第二列数据转换为数字类型
#df[df.columns[1]] = df[df.columns[1]].str.replace(',', '')
#df[df.columns[1]] = pd.to_numeric(df[df.columns[1]])
# 去除逗号和所有非数字字符，保留小数点
df[df.columns[1]] = df[df.columns[1]].str.replace(r'[^\d.]', '')
# 尝试将字符串转换为数字，无法转换的值将被设置为NaN
df[df.columns[1]] = pd.to_numeric(df[df.columns[1]], errors='coerce')


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