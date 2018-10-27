#coding=utf-8
import json
import requests
import re
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import lxml
import time
def get_one_page(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/69.0.3497.100 Safari/537.36'}
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RecursionError:
        return None

def parse_one_page(html):
    soup = BeautifulSoup(html,"lxml")
    dd = soup.find_all("dd")
    all_movie = []
    for tag in dd:
        content = {}
        tag_i = tag.find("i")
        content["range"] = tag_i.string
        tag_a = tag.find("a")
        content["name"] = tag_a["title"]
        all_movie.append(content)
    print(all_movie)
    return all_movie

def write_to_file(content):
    with open('result.txt','a',encoding="utf-8") as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)