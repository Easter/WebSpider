from urllib.parse import urlencode
from pyquery import PyQuery as pq
import requests
'''
    爬虫之Ajax数据爬取(js动态渲染并非只有Ajax这一种)，由于数据库还未开始学习，本文不将结果加入到数据库中，待以后更新
'''
base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host':'m.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def parse_page(json):
    if json:
        items = json.get('data').get('cards')#get为字典的方法
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()#利用pyquery去掉原文中的HTML标签元素
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo#此函数将不再是一个简单的函数，加入yield语句后变成了一个生成器(特殊的迭代器)，此此例中返回字典。

def parse_page1(json):
    if json:
        items = json.get('data').get('cards')
        del items[1]
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo

def get_page(page):
    params = {
        'type':'uid',
        'value':'2830678474',
        'containerid':'1076032830678474',
        'page':page
    }
    url = base_url+urlencode(params)#urllib的urlencode()方法等高级用法要熟练掌握
    try:
        response = requests.get(url,headers=headers)
        if response.status_code==200:
            print("ok")
            #print(response.json())
            return response.json()
    except requests.ConnectionError as e:
        print('ERROR',e.args)

if __name__ == '__main__':
    for page in range(1,11):
        if page == 1:#page为1的时候页面中插入了非微博文件需要特殊处理
            json = get_page(page)
            results = parse_page1(json)
            for result in results:
                print(result)
        else:
            json = get_page(page)
            results = parse_page(json)
            for result in results:
                print(result)
