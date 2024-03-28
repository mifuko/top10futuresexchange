from bs4 import BeautifulSoup
import pandas as pd

# 定义列名
column_names = ['名次', '会员号', '会员简称', '成交量（手）', '名次', '会员号', '会员简称', '成交额（万元）']

# 读取文本文件内容
with open('output.txt', 'r', encoding='utf-8') as file:
    page_source = file.read()

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(page_source, 'html.parser')

# 找到包含所需数据的表格，这里我们选择第一个'table'标签
table = soup.find('table', id='tab1')

# 提取表格的头部和身体部分
# 由于我们已经有了列名，这里不需要从HTML中提取headers
# headers = [th.get_text().strip() for th in table.find('thead').find_all('td')]

# 提取表格身体部分的前11行数据
rows_data = []
for tr in table.find('tbody').find_all('tr')[:11]:
    row_data = [td.get_text().strip() for td in tr.find_all('td')]
    rows_data.append(row_data)

# 创建DataFrame
df = pd.DataFrame(rows_data, columns=column_names)

# 打印DataFrame
print(df)
