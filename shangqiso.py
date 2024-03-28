# coding=utf-8
import time
import shutil
from selenium import webdriver
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

shfeurl = "https://www.shfe.com.cn/statements/dataview.html?paramid=pm"



options = webdriver.ChromeOptions()
#driver_path ="D:\chromedriver_win32 (1)\chromedriver.exe"
driver_path ="D:\chromedriver-win32\chromedriver.exe"

driver = webdriver.Chrome(driver_path, options=options)
driver.get(shfeurl)
driver.implicitly_wait(10)

js_noread = 'document.getElementById("dateinput").removeAttribute("readonly");'
driver.execute_script(js_noread)
time.sleep(2)
driver.find_element_by_id("dateinput").clear()
time.sleep(2)

wdate = "2024-03-27"

driver.maximize_window()
driver.find_element_by_id("dateinput").clear()
driver.find_element_by_id("dateinput").send_keys(wdate)
time.sleep(3)

driver.find_element_by_id("li_all").click()
time.sleep(2)

driver.find_element_by_class_name("excel_pic").click()
time.sleep(1)

shutil.move('C:/Users/kidor/Downloads/data.csv', 'D:/origin_shfe/shfeqh'+wdate+'.csv')
time.sleep(1)


plt.rcParams['font.sans-serif'] = ['SimHei']

# 创建 brokerlist 列表
brokerlist = ['东证期货', '中信期货', '海通期货', '华泰期货', '国泰君安', '方正中期',
              '永安期货', '五矿期货', '南华期货', '金瑞期货', '浙商期货', '光大期货',
              '银河期货', '广发期货', '国信期货', '国投安信', '国联期货', '东方财富',
              '中辉期货', '宝城期货']

# 读取 CSV 文件，并选择第 2 和第 9 列

data = pd.read_csv('D:/origin_shfe/shfeqh'+wdate+'.csv', usecols=[1, 2], header=1)
data['总成交量'] = pd.to_numeric(data['总成交量'], errors='coerce')

# 定义一个字典，用于记录每个经纪人的交易额
broker_sum = {}

# 对于属于经纪人名单中的第一列数据，对应的第二列数值相加
for index, row in data.iterrows():
    if row[0] in brokerlist:
        # 将字符串转换为浮点数或整数
        value = float(row[1])  # 或者 int(row[1])
        # 统计每个经纪人的交易额
        if row[0] not in broker_sum.keys():
            broker_sum[row[0]] = value
        else:
            broker_sum[row[0]] += value


df = pd.DataFrame(list(broker_sum.items()), columns=['broker', 'sum'])
df_sorted = df.sort_values('sum', ascending=False)
top_10 = df_sorted.head(10)

print(top_10)

# 绘制条形图并指定刻度格式和标签字体
ax = top_10.plot(kind='bar', x='broker', y='sum')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.1f}万'.format(x / 10000)))
ax.set_xticklabels(top_10['broker'])
ax.get_yaxis().set_label_coords(-0.1, 0.9)
plt.title('上期所'+wdate+'成交量前十的经纪商')
plt.show()
