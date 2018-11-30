import json
import os
from bs4 import BeautifulSoup
from multiprocessing import Pool
from langyi import _get_request, HOST


def get_detail(url, file_id, task_id):
    dir_path = os.path.join(os.getcwd(), 'langyi')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    r_path = os.path.join(dir_path, '%d_%d.json' % (file_id, task_id))
    if os.path.exists(r_path):
        print('%d_%d.json is exist! ' % (file_id, task_id))
        return
    result_list = list()
    r = _get_request(url)
    soup = BeautifulSoup(r, 'lxml')
    conright_list = soup.find_all('div', 'conright fr')
    for c in conright_list:
        s = c.text.strip()
        # s = s.replace(' ', '')
        result_list.append(s.strip())
        # print(s)
    conright_list = soup.find_all('div', 'conright fl')
    for c in conright_list:
        s = c.text.strip()
        # s = s.replace(' ', '')
        result_list.append(s.strip())
        # print(s)

    with open(r_path, 'w', encoding='utf-8') as fw:
        json.dump(result_list, fw)
    print('%d_%d.json is done! ' % (file_id, task_id))


def my_test():
    path = os.path.join(os.getcwd(), 'path', '1.json')
    with open(path, 'r') as fr:
        js = json.load(fr)
    for p in js:
        url = HOST+p['href']
        print(url)
        get_detail(url, 1, 0)
        break


def safe_get_detail(url, file_id, task_id):
    try:
        get_detail(url, file_id, task_id)
    except Exception as e:
        print(e)


def process_a_file(file_id):
    pool = Pool(8)
    path = os.path.join(os.getcwd(), 'path', '%d.json' % file_id)
    with open(path, 'r') as fr:
        js = json.load(fr)
    for n, p in enumerate(js):
        url = HOST + p['href']
        # print(url)
        # get_detail(url, file_id, n)
        pool.apply_async(safe_get_detail, args=(url, file_id, n))
    pool.close()
    pool.join()


if __name__ == '__main__':
    for i in range(1, 1001):
        process_a_file(i)
    # my_test()

