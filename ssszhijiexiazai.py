import wget
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

pickdatey = '2024'
pickdatem = '03'
pickdated = '26'

instruments = ['IF', 'IC', 'IM', 'IH', 'TS', 'TF', 'T', 'TL', 'IO', 'MO', 'HO']
for ins in instruments:
    url = 'http://www.cffex.com.cn/sj/ccpm/'+pickdatey+pickdatem+'/'+pickdated+'/'+ins+'_1.csv'
    downfile = 'D:/origin_download/'+ins+pickdatey+pickdatem+pickdated+'.csv'
    wget.download(url, downfile)

# 指定 CSV 文件所在的目录
directory = 'D:/origin_download/'

# 获取所有 CSV 文件的文件名
csv_files = glob.glob(os.path.join(directory, '*'+pickdatey+pickdatem+pickdated+'.csv'))

dfs = []
for csv_file in csv_files:
    # 使用 'utf-8', 'gbk', 'big5' 等多种编码方式尝试读取文件
    try:
        dfs.append(pd.read_csv(csv_file, encoding='utf-8'))
    except UnicodeDecodeError:
        try:
            dfs.append(pd.read_csv(csv_file, encoding='gbk'))
        except UnicodeDecodeError:
            dfs.append(pd.read_csv(csv_file, encoding='big5'))

# 将列表中的 DataFrame 进行合并
merged_df = pd.concat(dfs)

# 将合并后的 DataFrame 输出为一个新的 CSV 文件
merged_df.to_csv('D:/origin_download/merged.csv', index=False)

# 创建 brokerlist 列表
brokerlist = ['东证期货(经纪)', '华泰期货(经纪)', '南华期货(经纪)', '中信建投(经纪)', '招商期货(经纪)', '中泰期货(经纪)', '银河期货(经纪)',
              '中信建投(经纪)', '国泰君安(经纪)', '海通期货(经纪)', '申银万国(经纪)', '国信期货(经纪)', '方正中期(经纪)', '光大期货(经纪)',
              '东吴期货(经纪)', '平安期货(经纪)', '华安期货(经纪)', '浙商期货(经纪)', '广发期货(经纪)', '宏源期货(经纪)']

# 读取 CSV 文件，并选择第 2 和第 9 列
df = pd.read_csv('D:/origin_download/merged.csv', usecols=[2, 9], header=1)

# 建立新的 DataFrame，以 brokerlist 列表为基础
new_df = pd.DataFrame({'brokerlist': brokerlist})

print(df)

# 遍历 brokerlist，并在 new_df 的 'brosum' 列中填入每个经纪商的成交量总和
for i, bro in enumerate(brokerlist):
    broker = df.loc[df['会员简称'] == bro].copy()
    broker['成交量'] = pd.to_numeric(broker['成交量'], errors='coerce')
    brosum = broker['成交量'].sum()
    new_df.loc[i, 'brosum'] = brosum

# 输出新的 DataFrame
#print(new_df)

# 根据 brosum 降序排列
new_df = new_df.sort_values(by='brosum', ascending=False)

# 选取前 10 个经纪商
new_df = new_df.head(10)
#print(new_df)

# 按照 brokerlist 绘制柱状图
plt.bar(new_df['brokerlist'], new_df['brosum'], width=0.8)

# 调整 X 轴标签的旋转角度，以避免标签重叠
plt.xticks(rotation=30, ha='right')

# 添加 X 轴和 Y 轴标签
plt.xlabel('经纪商')
plt.ylabel('成交量总和')

# 添加标题
plt.title('中金所'+pickdatey+pickdatem+pickdated+'成交量前10的经纪商')

# 显示图形
plt.show()
