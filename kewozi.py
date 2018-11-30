import json
import os
import requests
import random
from bs4 import BeautifulSoup
from multiprocessing import Pool


PROXY = {'http': 'http://DONGNANHTT1:T74B13bQ@http-proxy-sg2.dobel.cn:9180',
         'https': 'http://DONGNANHTT1:T74B13bQ@http-proxy-sg2.dobel.cn:9180'}
_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',}
_SESSION = requests.session()
HOST = 'https://club.autohome.com.cn/'


def _get_request(url, param=None):
    resp = _SESSION.get(
        url,
        params=param,
        headers=_HEADERS,
        proxies=PROXY,
        # verify=False,
        timeout=random.choice(range(30, 100))
    )
    resp.encoding = resp.apparent_encoding
    # "utf-8"
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


# 获取标题及地址
def index_page_parser(page):
    r_path = os.path.join(os.getcwd(), 'kewozi_path', '%d.json' % page)
    if os.path.exists(r_path):
        print('page %d is already exist' % page)
        return
    # page = 1000
    page_list = list()
    url = 'https://club.autohome.com.cn/bbs/forum-c-4105-%d.html' % page
    r = _get_request(url)
    soup = BeautifulSoup(r, 'lxml')
    soup = soup.find_all('div', id='subcontent')[0]
    list_dl = soup.find_all('dl', 'list_dl')
    for i in list_dl:
        if len(i['class']) > 1:
            continue
        a = i.find_all('a', 'a_topic')
        if len(a) == 1:
            a = a[0]
        else:
            break
        t_dict = dict(lang=i['lang'],
                      href=a['href'],
                      title=a.text.strip())
        # print('--------------')
        # print(t_dict)
        page_list.append(t_dict)
        # print('--------------')
    dir_path = os.path.join(os.getcwd(), 'kewozi_path')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    path = os.path.join(dir_path, '%d.json' % page)
    with open(path, 'w') as fw:
        json.dump(page_list, fw)
    print('page: %d done' % page)


# 获取一个页面上所有帖子的连接
def get_url_list(page):
    pass


def safe_index_page_parser(page):
    try:
        index_page_parser(page)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pool = Pool(8)
    for i in range(1, 604+1):
        # index_page_parser(i)
        pool.apply_async(safe_index_page_parser, args=(i,))
    pool.close()
    pool.join()
