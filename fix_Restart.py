import os
import re
import requests
import time
import random

# 待修复的地址BookPath,适用于续传
# BookPath = r'E:\Storage\Book\Manga\Hanime\spider1\Book'
BookPath = r'E:\Storage\Book\Manga\Hanime\A单行本\A精细'
useurl = f'https://i.nhentai.net/galleries/'
fixFilePath = r'E:\Storage\Book\Manga\Hanime\spider1\fix_wait.txt'


def is_complete_jpeg(file_path):
    """ 检查JPEG文件是否完整 """
    try:
        with open(file_path, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            return f.read() == b'\xff\xd9'
    except Exception as e:
        return False


def is_complete_png(file_path):
    """ 检查PNG文件是否完整 """
    try:
        with open(file_path, 'rb') as f:
            f.seek(-8, os.SEEK_END)
            return f.read() == b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    except Exception as e:
        return False


def check_and_generate_download_links(book_path):
    """ 检查图片完整性，生成下 """
    incomplete_files = []
    for root, dirs, files in os.walk(book_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.jpg') and not is_complete_jpeg(file_path):
                incomplete_files.append(file_path)
                if file.endswith('.png') and not is_complete_png(file_path):
                    incomplete_files.append(file_path)

    with open(fixFilePath, 'w') as fix_file:
        for file_path in incomplete_files:
            file_name = os.path.basename(file_path)
            match = re.search(r'(\d+)', file_name)
            if match:
                file_number = match.group(1)
                gallery_id = os.path.basename(os.path.dirname(file_path))
                fix_file.write(f'{gallery_id}/{file_number}\n')
            else:
                print(f"文件名中未找到数字: {gallery_id}/{file_number}/{file_name}")
                pass


def download(file_path, picture_url):
    """ 下载jpg图片并检查完整性，如不完整则重试 """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 2
    for i in range(max_retries):
        try:
            r = requests.get(picture_url, headers=headers, stream=True)
            if r.status_code == 404:
                return False
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                if is_complete_jpeg(file_path):
                    return True
        except requests.exceptions.RequestException as e:
            pass
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)
    return False


def download2(file_path, picture_url):
    """ 下载png图片并检查完整性，如不完整则重试 """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 8
    for i in range(max_retries):
        try:
            r = requests.get(picture_url, headers=headers, stream=True)
            if r.status_code == 404:
                return False
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                if is_complete_png(file_path):
                    return True
        except requests.exceptions.RequestException as e:
            pass
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)
    return False


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"已删除文件: {file_path}")


def main():
    with open(fixFilePath, 'r') as f:
        lines = f.readlines()
    for line in lines:
        m, start_page = line.strip().split('/')
        m = int(m)
        start_page = int(start_page)
        prefix_url = f'{useurl}{m}/'
        webname = str(m)
        os.makedirs(os.path.join(BookPath, webname), exist_ok=True)
        print(f'开始修复{m}/{start_page}')
        file_path = os.path.join(BookPath, webname, f'{start_page}.jpg')
        picture_url = f'{prefix_url}{start_page}.jpg'
        if not download(file_path, picture_url):
            file_path = os.path.join(BookPath, webname, f'{start_page}.png')
            picture_url = f'{prefix_url}{start_page}.png'
            if not download2(file_path, picture_url):
                pass


if __name__ == '__main__':
    main()
