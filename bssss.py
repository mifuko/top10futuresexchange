import asyncio
import random
from pyppeteer import launch
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd

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
    url = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/2024/20240327/FutureDataTradeamt.htm"
    await page.goto(url, {'waitUntil': 'networkidle2'})

    # 滚动页面并等待
    await scroll_page(page)
    await wait_random_time()

    # 再次滚动页面并等待
    await scroll_page(page)
    await wait_random_time()

    # 刷新网页
    await page.reload({'waitUntil': 'networkidle2'})

    # 读取网页源代码
    page_source = await page.content()
#    print(page_source)
    with open('output.txt', 'w', encoding='utf-8') as file:
        # 将page_source的内容写入文件
        file.write(page_source)
    # 刷新网页
    await page.reload({'waitUntil': 'networkidle2'})

    # 关闭浏览器
#    await browser.close()

# 启动事件循环
asyncio.get_event_loop().run_until_complete(main())