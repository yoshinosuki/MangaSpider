# /**
#  * Filename            :   Get_Book_1_auto.py
#  * Author              :   Wang Xiang
#  * Description         :   网络爬虫
#  * Revision History    :   24-03-19
#  * Revision            :   2.1
#  */

import os
import requests
import time


# 下载
def download(file_path, picture_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 8  # 最大重试次数
    for i in range(max_retries):
        try:
            r = requests.get(picture_url, headers=headers)
            with open(file_path, 'wb') as f:
                f.write(r.content)
            break  # 如果下载成功，退出循环
        except requests.exceptions.RequestException as e:
            print(f'download Retry {i + 1}/{max_retries} after {e}')
            time.sleep(2)  # 延迟重试


# 请求判断
def main():
    with open('./List/Target_auto.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        m = int(line.strip())  # 从每行读取的数字
        webname = str(m)  # 直接使用读取的数字作为文件夹名称
        os.makedirs('../Book/' + webname + '/', exist_ok=True)  # 输出目录

        n = 1000  # 该类目下的图片下载最大数
        for i in range(1, n + 1):
            file_path_jpg = '../Book/' + webname + '/' + str(i) + '.jpg'
            file_path_png = '../Book/' + webname + '/' + str(i) + '.png'
            picture_url_jpg = 'https://i5.nhentai.net/galleries/' + webname + '/' + str(i) + '.jpg'
            picture_url_png = 'https://i5.nhentai.net/galleries/' + webname + '/' + str(i) + '.png'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
            }
            max_retries2 = 8  # 最大重试次数
            for t in range(max_retries2):
                try:
                    r = requests.head(picture_url_jpg, headers=headers)
                    if r.status_code == 404:
                        output = '已完成' + webname
                        print(output)
                        break
                    else:
                        if r.status_code == 200:
                            picture_url = picture_url_jpg
                            file_path = file_path_jpg
                            download(file_path, picture_url)
                            time.sleep(1.5)
                        else:
                            picture_url = picture_url_png
                            file_path = file_path_png
                            download(file_path, picture_url)
                            time.sleep(1.5)

                except requests.exceptions.RequestException as e:
                    print(f'Get Request Retry {t + 1}/{max_retries2} after {e}')
                    if t >= 6:
                        print(f'check network connections')
                    time.sleep(2)


if __name__ == '__main__':
    main()
