import asyncio
from pyppeteer import launch

async def main():
    # 启动浏览器
    browser = await launch()
    page = await browser.newPage()

    # 增加超时时间到60秒
    await page.goto("http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html", {'waitUntil': 'networkidle2', 'timeout': 60000})
    # 等待页面上的日期选择器加载完成
    await page.waitForSelector('#control select:nth-of-type(1)')
    await page.waitForSelector('#control select:nth-of-type(2)')

    # 模拟用户选择年份和月份
    await page.select('#control select:nth-of-type(1)', '2024')
    await page.select('#control select:nth-of-type(2)', '02')

    # 更改currDate输入框的值以模拟选择新的日期
    new_date_value = '20240215'  # 新日期值，格式为YYYYMMDD
    await page.evaluate(f"document.getElementById('currDate').value = '{new_date_value}';")

    # 等待页面内容更新
    await page.waitFor(1000);  # 等待1秒

    # 获取并打印修改后的页面内容
    new_page_content = await page.content()
    print(new_page_content)

    # 关闭浏览器
    await browser.close()


# 运行异步函数
asyncio.get_event_loop().run_until_complete(main())
