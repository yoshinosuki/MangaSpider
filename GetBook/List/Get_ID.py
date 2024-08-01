from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

def get_html_selenium(url):
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1)  # Allow some time for the page to load
    html = driver.page_source
    driver.quit()
    return html

def parse_html(html_text):
    picre = re.compile(r'[a-zA-z]+://[^\s]*\.jpg')  # This regex gets URLs ending with .jpg
    pic_list = []
    for pic_url in picre.findall(html_text):
        match = re.search(r'\d{5,}', pic_url)
        if match:
            pic_list.append(match.group())
    return pic_list

def main():
    for page in range(1, 2):
        url = 'https://nhentai.net/tag/uncensored/?page=' + str(page)
        html_text = get_html_selenium(url)
        with open('123.txt', 'a') as f:
            f.write(html_text)
        pic_list = parse_html(html_text)
        with open('ID.txt', 'a') as f:
            for pic_url in pic_list:
                f.write(pic_url + '\n')
        time.sleep(1)  # Respectful crawling by spacing requests

if __name__ == '__main__':
    main()
