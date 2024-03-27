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
soupdce = BeautifulSoup(dcepage, 'html.parser')

# 找到包含数据的表格
table = soupdce.find('table')
if table:
    # 尝试找到<thead>和<tbody>标签
    headers = table.find_all('thead')[0] if table.find('thead') else table.find_all('tr')[0]
    header = [th.get_text(strip=True) for th in headers.find_all('th')]

    # 初始化存储数据的列表
    rows = [header]  # 将表头添加到rows列表中

    # 计数器，用于跟踪当前行号
    counter = 0
    # 遍历<tbody>中的所有<tr>标签，但只取前12行
    tbody = table.find('tbody') if table.find('tbody') else table
    for tr in tbody.find_all('tr')[:12]:  # 从所有<tr>标签中取前12行
        tddata = tr.find_all('td')
        if tddata:
            row_data = [td.get_text(strip=True) for td in tddata]
            rows.append(row_data)
            counter += 1
        if counter >= 11:  # 达到12行后停止遍历
            break
else:
    print("警告：未找到<table>标签。")

# 将数据转换为pandas DataFrame
df = pd.DataFrame(rows[1:], columns=header) if header else None  # 确保header不为空

# 打印DataFrame
print(df)


""" 绘制条形图并指定刻度格式和标签字体
ax = top_10.plot(kind='bar', x='会员简称', y='成交量（手）')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.1f}万'.format(x / 10000)))
ax.set_xticklabels(top_10['会员简称'])
#ax.set_ylabel('成交量（万手）', fontweight='bold', rotation=90, labelpad=20)
ax.get_yaxis().set_label_coords(-0.1, 0.9)

# 显示图形
plt.show()
"""