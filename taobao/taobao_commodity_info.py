#coding=utf-8
'''
本篇并没有进行反爬虫策略，很有可能被检测到是爬虫而被进行验证
还有开始爬之前需要进行网页登陆，本页也没有编写，待以后更新
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq

browser = webdriver.Chrome()
wait = WebDriverWait(browser,20)
KEY_WORD = "多开"
MAX_PAGE = 10

def index_page(page):
    print("正在爬取第",page,"页")
    try:
        url = 'https://s.taobao.com/search?q='+quote(KEY_WORD)
        browser.get(url)
        if page>1:
            input = wait.until(#如果该节点加载出来就返回这个节点，网速好的朋友可忽略
                EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > '
                                                            'span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)

def get_products():
    '''
    提取商品数据
    '''
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'title':item.find('.J_ClickStat').text(),
            'image':item.find('.pic .img').attr('data-src'),
            'price':item.find('.price').text(),
            'location':item.find('.location').text(),
            'shop':item.find('.shop').text()
        }
        print(product)

def main():
    for i in range(1,MAX_PAGE+1):
        index_page(i)
    browser.close()

main()