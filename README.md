2024-03-27

淦郑商所网页改了，在`bssss.py`中BeautifulSoup和urllib不得行了，报错:

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


尝试用mobile地址，```czce.com.cn/cn/jysj/cjpm/H770305index_1.htm```尝试把这个网页发给两台手机，发现第一次点开都报错，不会显示真正的内容，链接变成了```http://www.czce.com.cn/cn/jysj/cjpm/H770305index\_1.htm?3TxcOVKoEO7I=1711526673863```，但是第二次再点进去就可以正常打开
只能尝试用cookie的方式

成功打开了！！！！！！！！但是点不到按钮估计找不到button，打算重新回最初的链接，只要能打开，从纯表格里面找就不用按钮了！！！！！！！！
```
import asyncio
import random
import time
from pyppeteer import launch
from fake_useragent import UserAgent

async def main():
    # 引入random模块
    random.seed()

    # 创建一个随机用户代理对象
    ua = UserAgent()

    # 启动浏览器
    browser = await launch({
        'headless': False,  # 设置为 True 启用无头模式
        'args': [
            '--disable-blink-features=AutomationControlled',  # 禁用 WebDriver 标志
            '--disable-infobars',
            f'--user-agent={ua.random}',  # 设置随机用户代理
        ]
    })
    page = await browser.newPage()

    time.sleep(1)
    # 设置窗口大小
    await page.setViewport({"width": random.randint(1024, 1920), "height": random.randint(768, 1080)})

    # 设置Cookie
    cookie = {"name": "UM_distinctid", "value": "18e7f0c1f2627-04b2b8c6824753-6755742d-144000-18e7f0c1f28a0c", "domain": ".czce.com.cn"}
    await page.setCookie(cookie)

    # 访问目标网页
    url = "http://www.czce.com.cn/cn/jysj/cjpm/H770305index_1.htm"
    await page.goto(url, {'waitUntil': 'networkidle0'})
    time.sleep(10)
    # 等待页面加载完成
    await page.waitForXPath('//table')
    time.sleep(1)
    # 执行一些随机操作
    await page.evaluate('''() => {
        window.scrollTo(0, document.body.scrollHeight / 2);
    }''')
    time.sleep(3)
    # 找到"导出 EXCEL"链接并点击
    link = await page.waitForXPath("//a[contains(@onclick, 'FutureDataTradeamt')]")
    await link.click()
    time.sleep(5)
    # 等待文件下载完成(根据实际情况调整等待时间)
    await asyncio.sleep(10)

    # 关闭浏览器
    await browser.close()

# 启动事件循环
asyncio.get_event_loop().run_until_complete(main())

```

淦找ip也不行，这个版本在不开代理的情况下，时灵时不灵的

```
import asyncio
import random
from pyppeteer import launch
from fake_useragent import UserAgent

async def read_table_content(page):
    # 确保页面加载完成
    await page.waitForSelector('#hdtab1 table', {'timeout': 30000})  # 增加等待时间至30秒

    # 使用JavaScript获取表格内容
    table_content = await page.evaluate('''() => {
        const table = document.querySelector('#hdtab1 table');
        let rows = [];
        for (let i = 1; i < table.rows.length; i++) { // 跳过表头
            let row = [];
            for (let j = 0; j < table.rows[i].cells.length; j++) {
                row.push(table.rows[i].cells[j].innerText.trim());
            }
            rows.push(row);
        }
        return rows;
    }''')

    return table_content

async def main():
    ua = UserAgent()
    browser = await launch({
        'headless': False,  # 设置为 True 启用无头模式
        'args': [
            '--disable-blink-features=AutomationControlled',  # 禁用 WebDriver 标志
            '--disable-infobars',
            f'--user-agent={ua.random}',  # 设置随机用户代理
        ]
    })
    page = await browser.newPage()

    # 设置窗口大小
    await page.setViewport({"width": random.randint(1024, 1920), "height": random.randint(768, 1080)})

    # 设置Cookie
    cookie = {"name": "UM_distinctid", "value": "18e7f0c1f2627-04b2b8c6824753-6755742d-144000-18e7f0c1f28a0c", "domain": ".czce.com.cn"}
    await page.setCookie(cookie)

    # 访问目标网页
    url = "http://www.czce.com.cn/cn/jysj/cjpm/H770305index_1.htm"
    await page.goto(url, {'waitUntil': 'networkidle2'})


# 启动事件循环
asyncio.get_event_loop().run_until_complete(main())

```

——————————————————————————————————————————————————————————

20240328


好消息，成功读到了网页源代码

坏消息，源代码里面没有我需要的表格

只能读到这个地址的内容，读不到单独表格url的网页源代码，单独表格url的网页源代码只能得到`<html><head></head><body></body></html>`

还是要尝试java同步直接按按钮

```
import asyncio
import random
from pyppeteer import launch
from fake_useragent import UserAgent

# 引入fake_useragent中的UserAgent类
ua = UserAgent()

async def scroll_page(page):
    # 滚动到页面底部
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    # 等待页面滚动完成
    await asyncio.sleep(1)

async def wait_random_time():
    # 随机等待一段时间，模拟真实用户操作
    await asyncio.sleep(random.uniform(1, 3))

async def main():
    # 随机选择一个移动设备的User-Agent
    mobile_user_agent = ua.random

    browser = await launch({
        'headless': False,
        'args': [
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            f'--user-agent={mobile_user_agent}',
        ]
    })
    page = await browser.newPage()

    # 设置窗口大小
    await page.setViewport({"width": random.randint(1024, 1920), "height": random.randint(768, 1080)})

    # 设置Cookie
    cookie = {"name": "UM_distinctid", "value": "18e7f0c1f2627-04b2b8c6824753-6755742d-144000-18e7f0c1f28a0c", "domain": ".czce.com.cn"}
    await page.setCookie(cookie)

    # 访问目标网页
    url = "http://www.czce.com.cn/cn/jysj/cjpm/H770305index_1.htm"
    await page.goto(url, {'waitUntil': 'networkidle2'})

    # 滚动页面并等待
    await scroll_page(page)
    await wait_random_time()

    # 再次滚动页面并等待
    await scroll_page(page)
    await wait_random_time()

    # 读取网页源代码
    page_source = await page.content()
    print(page_source)

    # 关闭浏览器
    await browser.close()

# 启动事件循环
asyncio.get_event_loop().run_until_complete(main())
```
