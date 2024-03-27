from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# 指定chromedriver的路径
driver_path = "D:\chromedriver-win64\chromedriver.exe"

# 创建Chrome选项对象
options = Options()
# 设置无头模式，这样不会打开浏览器窗口
options.add_argument("--headless")

# 初始化WebDriver
driver = webdriver.Chrome(driver_path, options=options)

# 访问指定的网页
url = "http://www.gfex.com.cn/gfex/jdcjpm/hqsj_tjsj.shtml"  # 替换为您想要抓取的网页URL
driver.get(url)

# 等待页面加载完成
wait = WebDriverWait(driver, 40)

# 滚动到页面底部，确保所有内容都已经加载
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 等待特定的表格元素可见
is_element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.layui-table-body.layui-table-main"))
wait.until(is_element_present)

# 直接通过JavaScript获取表格HTML
table_html = driver.execute_script("return document.querySelector('div.layui-table-body.layui-table-main').innerHTML;")

# 创建BeautifulSoup对象解析HTML
soup = BeautifulSoup(table_html, 'html.parser')

# 找到所有的行<tr>元素
rows = soup.find_all('tr')

# 定义列名
columns = ['名次', '会员号', '会员名称', '成交量', '成交量比重', '名次', '会员号', '会员名称', '成交额', '成交额比重']

# 初始化空的DataFrame
df = pd.DataFrame(columns=columns)

# 遍历每一行，从第一个开始
for index, row in enumerate(rows):
    # 获取每个单元格<td>元素的文本
    cols = row.find_all('td')
    cols_text = [ele.get_text(strip=True) for ele in cols]

    # 确保行数和列数匹配
    if len(cols_text) == len(columns):
        # 将单元格文本添加到DataFrame中
        df.loc[index] = cols_text

# 打印DataFrame
print(df.head(10))

# 关闭浏览器
driver.quit()