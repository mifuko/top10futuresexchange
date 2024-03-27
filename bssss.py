from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox") # linux only
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_cdp_cmd("Network.enable", {})
    time.sleep(1)
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    time.sleep(1)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver


def scrape_table():
    url = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/2024/20240326/FutureDataTradeamt.htm"
    driver = None

    try:
        driver = getDriver()
        driver.get(url)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        # 等待表格加载完成
        wait = WebDriverWait(driver, 40)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tab1 tr")))

        # 获取网页源码并用BeautifulSoup解析
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 查找ID为"tab1"的表格及其tbody部分
        table = soup.find(id="tab1")
        tbody = table.find('tbody')

        # 解析表格数据
        table_rows = tbody.find_all('tr')

        # 输出前几行数据
        for i, row in enumerate(table_rows[:3]):
            print(f"行 {i + 1}: {row}")

    except Exception as e:
        print(f"抓取过程中发生错误: {str(e)}")
        if hasattr(driver, 'status_code'):  # 此处实际上driver不会有status_code属性，因为它是WebDriver对象
            return driver.status_code
        else:
            return "未知错误"

    finally:
        if driver is not None:
            driver.quit()


scraped_data_or_error = scrape_table()