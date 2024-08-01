import csv
import os
import re
import requests
import time
from bs4 import BeautifulSoup

def get_html(url, max_retries=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    }
    for i in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            html = response.text
            return html
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f'Retry {i+1}/{max_retries} after {e}')
            time.sleep(2**(i+1))
    raise Exception(f'Failed to get HTML after {max_retries} retries')

def parse_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    div_list = soup.find_all('div', class_='comic-rows-videos-title')
    title_list = []
    for div in div_list:
        title = div.text.strip()
        title_list.append(title)
    return title_list

def main():
    with open('Title.txt', 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'title'])  # 写入标题行
        for page in range(1, 2):
            url = 'https://nhentai.net/tag/uncensored/?page=' + str(page)
            html_text = get_html(url)
            title_list = parse_html(html_text)
            for i, title in enumerate(title_list, start=1):
                writer.writerow([i, title])
            time.sleep(0.6)

if __name__ == '__main__':
    main()
