import json
import os
from langyi import HOST

def page_merge(page):
    # content = list()
    i_path = os.path.join(os.getcwd(), 'path', '%d.json' % page)
    with open(i_path, 'r') as fr:
        p_list = json.load(fr)
    print(len(p_list))
    for n, p in enumerate(p_list):
        c_path = os.path.join(os.getcwd(), 'langyi', '%d_%d.json' % (page, n))
        with open(c_path, 'r') as fr:
            content_n = json.load(fr)
        if p['title'] in content_n[0]:
            p['href'] = HOST+p['href']
            p['content'] = content_n

    m_path = os.path.join(os.getcwd(), 'langyi_merged')
    if not os.path.exists(m_path):
        os.makedirs(m_path)

    r_path = os.path.join(m_path, '%d.json' % page)
    with open(r_path, 'w') as fw:
        json.dump(p_list, fw)


def run():
    for i in range(1, 1001):
        page_merge(i)


if __name__ == '__main__':
    page_merge(1)
