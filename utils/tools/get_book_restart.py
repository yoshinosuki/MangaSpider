import os
import re
import requests
import time
import random
downloadPath = r'..\list\target_restart.txt'
BookPath = r'..\..\book'
useurl = f'https://i.nhentai.net/galleries/'

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 设置工作目录为脚本所在的目录
os.chdir(script_dir)


def is_complete_jpeg(file_path):
    """ 检查JPEG文件是否完整 """
    try:
        with open(file_path, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            return f.read() == b'\xff\xd9'
    except Exception as e:
        print(f"Error checking file completeness: {e}")
        return False


def is_complete_png(file_path):
    """ 检查PNG文件是否完整 """
    try:
        with open(file_path, 'rb') as f:
            f.seek(-8, os.SEEK_END)
            return f.read() == b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    except Exception as e:
        print(f"Error checking file completeness: {e}")
        return False


def download(file_path, picture_url):
    """ 下载jpg图片并检查完整性，如不完整则重试 """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 8  # 最大重试次数
    for i in range(max_retries):
        try:
            r = requests.get(picture_url, headers=headers, stream=True)
            if r.status_code == 404:
                print(f"File not found (404): {picture_url}")
                return False  # 404时退出
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                if is_complete_jpeg(file_path):
                    return True
                else:
                    print(f"File downloaded but incomplete, retrying: {file_path}")
                    pass
            else:
                print(f"Failed to download, status code: {r.status_code}")
                pass
        except requests.exceptions.RequestException as e:
            print(f'Retry {i + 1}/{max_retries} after {e}')
            pass
        sleep_time = random.uniform(1, 3)  # 生成1到3秒之间的随机睡眠时间
        time.sleep(sleep_time)  # 随机延迟重试
    return False


def download2(file_path, picture_url):
    """ 下载png图片并检查完整性，如不完整则重试 """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 8  # 最大重试次数
    for i in range(max_retries):
        try:
            r = requests.get(picture_url, headers=headers, stream=True)
            if r.status_code == 404:
                print(f"File not found (404): {picture_url}")
                return False  # 404时退出
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                if is_complete_png(file_path):
                    return True
                else:
                    print(f"File downloaded but incomplete, retrying: {file_path}")
                    if not is_complete_png(file_path):
                        print(f'File false.please check the photo')
                        return True

            else:
                print(f"Failed to download, status code: {r.status_code}")
                pass
        except requests.exceptions.RequestException as e:
            print(f'Retry {i + 1}/{max_retries} after {e}')
            pass
        sleep_time = random.uniform(1, 3)  # 生成1到3秒之间的随机睡眠时间
        time.sleep(sleep_time)  # 随机延迟重试
    return False


def get_max_file_number(directory):
    """ 获取目录中最大的文件序号 """
    max_num = 0
    for filename in os.listdir(directory):
        num = int(re.sub(r'\D', '', filename))  # 提取数字
        if num > max_num:
            max_num = num
    return max_num


def main():
    global webname
    with open(downloadPath, 'r') as f:
        lines = f.readlines()
    for line in lines:
        m = int(line.strip())
        prefix_url = f'{useurl}{m}/'
        match = re.search(r'galleries/(\d+)', prefix_url)
        if match:
            webname = str(m)
        os.makedirs(os.path.join(BookPath, webname), exist_ok=True)
        n = 3000  # 页数
        start_page = get_max_file_number(os.path.join(BookPath, webname)) + 1  # 获取起始页数
        """单点续传"""
        for i in range(start_page, n + 1):  # 从最大序号开始
            file_path = os.path.join(BookPath, webname, f'{i}.jpg')
            picture_url = f'{prefix_url}{i}.jpg'
            if not download(file_path, picture_url):
                file_path = os.path.join(BookPath, webname, f'{i}.png')
                picture_url = f'{prefix_url}{i}.png'
                if not download2(file_path, picture_url):
                    print(f'One Book Complete: {m}')
                    break


if __name__ == '__main__':
    main()
