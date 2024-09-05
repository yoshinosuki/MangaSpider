import random
import re
import time
import os
import argparse
import playwright
from playwright.sync_api import sync_playwright

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def get_html(page, url):
    page.goto(url, timeout=60000)  # 设置超时时间为 60 秒
    return page.content()


def parse_html(html_text):
    """ 筛选包含jpg的url """
    picre = re.compile(r'[a-zA-z]+://[^\s]*\.jpg')  # 本正则式得到.jpg结尾的url
    pic_list = []
    for pic_url in picre.findall(html_text):
        match = re.search(r'\d{5,}', pic_url)
        if match:
            pic_list.append(match.group())
    return pic_list


def main(url_prefix):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        time.sleep(5)

        for page_num in range(1, 6):  # 运行1~5页
            url = url_prefix + str(page_num)
            html_text = get_html(page, url)
            pic_list = parse_html(html_text)
            with open('.\list\id_new.txt', 'a') as f:
                for pic_url in pic_list:
                    f.write(pic_url + '\n')
            sleep_time = random.uniform(1, 3)
            time.sleep(sleep_time)

        browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='URLs.')
    parser.add_argument('url', type=str, nargs='?', default='https://nhentai.net/search/?q=uncensored+%5Bchinese%5D&page=', help='The URL prefix to use')
    # 无码uncensored 中文%5Bchinese%5D 大于60页pages%3A%3E60
    # 无码中文：https://nhentai.net/search/?q=uncensored+%5Bchinese%5D&page=
    # 无码中文单行本：https://nhentai.net/search/?q=pages%3A%3E60+uncensored+%5Bchinese%5D&page=
    # 中文单行本：https://nhentai.net/search/?q=pages%3A%3E100+%5Bchinese%5D&page=
    args = parser.parse_args()
    main(args.url)
