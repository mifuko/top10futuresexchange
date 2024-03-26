# coding=utf-8
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import shutil
import zipfile


dceurl = "http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html"
# dceurl = "http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/jdtj/rcjccpm/index.html"

options = webdriver.ChromeOptions()
driver_path ="D:\chromedriver_win32 (1)\chromedriver.exe"
driver = webdriver.Chrome(driver_path, options=options)

driver.get(dceurl)
driver.implicitly_wait(10)
driver.maximize_window()
sleep(1)

wmonth = '06'
wday = '16'

# 查找下拉框元素
#5月4日对应3
select_element = driver.find_element_by_css_selector("#control > select:nth-child(3)")

select = Select(select_element)
select.select_by_visible_text(wmonth)

# 查找所有 <td> 元素
td_elements = driver.find_elements_by_tag_name('td')

# 遍历每个 <td> 元素
for td_element in td_elements:
    # 判断元素的可见文本是否为 '08'
    if td_element.text == wday:
        # 创建 ActionChains 对象
        actions = ActionChains(driver)
        # 移动到元素并点击
        actions.move_to_element(td_element).click().perform()
        break

sleep(3)

a_element = driver.find_element_by_link_text("批量下载")
a_element.click()

sleep(5)
wait = WebDriverWait(driver, 10)
alert = wait.until(EC.alert_is_present())
#print(alert.text)

alert.accept()

search_box = driver.find_element_by_id('search_box')
search_box.send_keys('selenium')
search_box.send_keys(Keys.RETURN)

driver.close()




#————————————————————————————————————————————————————————————————————————————————————
# pick date
#select_element1 = driver.find_element_by_xpath('//*[@id="control"]/select[1]')
#selecty = Select(select_element1)
#selecty.select_by_value('2021')
#sleep(1)

#sel2 = driver.find_element_by_xpath('//*[@id="control"]/select[2]')
#selectm = Select(sel2)
#selectm.select_by_value(3)
#sleep(1)

# 定位 table 元素
#table = driver.find_element_by_class_name('week')

#td = driver.find_element_by_xpath('//td[contains(text(),"06")]')
#td.click()
#sleep(5)

