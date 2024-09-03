import random
import re
import time
from playwright.sync_api import sync_playwright


def get_html(page, url):
    page.goto(url)
    return page.content()


def parse_html(html_text):
    picre = re.compile(r'[a-zA-z]+://[^\s]*\.jpg')  # 本正则式得到.jpg结尾的url
    pic_list = []
    for pic_url in picre.findall(html_text):
        match = re.search(r'\d{5,}', pic_url)
        if match:
            pic_list.append(match.group())
    return pic_list


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for page_num in range(1, 5):
            # 无码 中文 大于60页
            # https://nhentai.net/search/?q=pages%3A%3E60+uncensored+%5Bchinese%5D&page=
            # https://nhentai.net/search/?q=uncensored+%5Bchinese%5D&page=
            url = 'https://nhentai.net/search/?q=uncensored+%5Bchinese%5D&page=' + str(page_num)
            html_text = get_html(page, url)
            pic_list = parse_html(html_text)
            with open('new.txt', 'a') as f:  # 使用追加模式打开文件，将结果追加到文件末尾
                for pic_url in pic_list:
                    f.write(pic_url + '\n')
            sleep_time = random.uniform(1, 3)  # 生成1到3秒之间的随机睡眠时间
            time.sleep(sleep_time)  # 添加随机延时，避免请求过于频繁被网站屏蔽

        browser.close()

if __name__ == '__main__':
    main()
