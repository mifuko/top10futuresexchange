2024-03-27

- 淦郑商所网页改了，在`bssss.py`中BeautifulSoup和urllib不得行了，报错:

```urllib.error.HTTPError: HTTP Error 412: Precondition Failed```

改了header之后，在console中发现直接被拒绝

```Failed to load resource: the server responded with a status of 400 (Bad Request)```

抓这个网页都失败了```http://www.czce.com.cn/cn/DFSStaticFiles/Future/2024/20240326/FutureDataTradeamt.htm```，换个思路直接从主页一路模拟鼠标点进去

还是不行。

存一版selenium的，就算是用了正常手工的agent也不行
```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 创建ChromeOptions对象
options = webdriver.ChromeOptions()

# 设置User-Agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')

# 指定ChromeDriver驱动程序路径
driver_path = r"D:\chromedriver-win32\chromedriver.exe"

# 创建Chrome浏览器实例并应用设置
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# 访问网页
url = "http://www.czce.com.cn/cn/jysj/cjpm/H770305index_1.htm"
driver.get(url)

# 等待页面加载完成
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

# 找到"导出EXCEL"链接并点击
link = driver.find_element_by_xpath("//a[contains(@onclick, 'FutureDataTradeamt')]")
link.click()

# 等待文件下载完成(根据实际情况调整等待时间)
time.sleep(10)

# 关闭浏览器
driver.quit()
```

存一版pyppeteer的
```
import asyncio
from pyppeteer import launch

async def main():
    # 启动浏览器
    browser = await launch({
        'headless': False,  # 设置为 True 启用无头模式
        'args': ['--disable-infobars']
    })
    page = await browser.newPage()

    # 设置用户代理字符串
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')

    # 访问目标网页
    url = "http://www.czce.com.cn/cn/jysj/cjpm/H770305index_1.htm"
    await page.goto(url, {'waitUntil': 'networkidle0'})

    # 等待页面加载完成
    await page.waitForXPath('//table')

    # 找到"导出 EXCEL"链接并点击
    link = await page.waitForXPath("//a[contains(@onclick, 'FutureDataTradeamt')]")
    await link.click()

    # 等待文件下载完成(根据实际情况调整等待时间)
    await asyncio.sleep(10)

    # 关闭浏览器
    await browser.close()

# 启动事件循环
asyncio.get_event_loop().run_until_complete(main())
```

- 上期所的`shangqiso.py`当天只能爬取前一天的，修改日期好像失效了，估计页面也有改动，但至少还能用

- 中金所的`ssszhijiexiazai.py`根据不同合约构建url还正常，得到`merged.csv`正常，但是计算top10的部分有问题，因为经纪商名字改了，在后面加了（经纪），需要修改这个字典

```
# 创建 brokerlist 列表
brokerlist = ['上海东证', '华泰期货', '南华期货', '中信建投', '招商期货', '中泰期货', '银河期货', 
              '中信期货', '国泰君安', '海通期货', '申银万国', '国信期货', '方正中期', '光大期货', 
              '东吴期货', '平安期货', '华安期货', '浙商期货', '广发期货', '宏源期货']
```

- 大商所的`ddds.py`最后获取结果有问题，页面直接显示top150，修改一下爬取的内容，舍弃成交额的排名，只保留成交量的排名

- 广期所的`ggfex.py`可以用，不落地，table在div里面，layui，官网不能开代理访问
