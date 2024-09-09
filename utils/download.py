import subprocess
import os
from concurrent.futures import ThreadPoolExecutor
import sys
import requests


def test_web():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 3  # 最大重试次数
    for i in range(max_retries):
        try:
            r = requests.get('https://nhentai.net', headers=headers, stream=True)
            if r.status_code == 200:
                print(f"网络测试成功")
                return True
        except requests.exceptions.RequestException as e:
            print(f'Retry {i + 1}/{max_retries} after {e}')
            pass
    print(f'网络连接失败')


def run_script(script):
    process = subprocess.Popen([sys.executable, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    with open('log.txt', 'a') as log_file:
        if stdout:
            log_file.write(stdout.decode('utf-8'))
        if stderr:
            log_file.write(stderr.decode('utf-8'))


def main():
    print("开始下载进程")
    path = "../book"
    os.makedirs(path, exist_ok=True)

    scripts = ["./tools/get_book_1.py", "./tools/get_book_2.py", "./tools/get_book_3.py"]

    with ThreadPoolExecutor() as executor:
        executor.map(run_script, scripts)

    print("下载完成，下载记录已保存")


if __name__ == '__main__':
    if test_web():
        main()
