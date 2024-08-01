import os
import re
import requests
import time

downloadPath = r'E:\Storage\Book\Manga\Hanime\spider1\GetBook\List\Target_png.txt'
BookPath = r'E:\Storage\Book\Manga\Hanime\spider1\Book'

def download(file_path, picture_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 8  # 最大重试次数
    for i in range(max_retries):
        try:
            r = requests.get(picture_url, headers=headers)
            with open(file_path, 'wb') as f:
                f.write(r.content)
            break  # 如果下载成功，退出循环
        except requests.exceptions.RequestException as e:
            print(f'Retry {i + 1}/{max_retries} after {e}')
            time.sleep(2 ** (i + 1))  # 指数增长的延迟重试

def main():
    with open(downloadPath, 'r') as f:
        lines = f.readlines()
    for line in lines:
        m = int(line.strip())
        prefix_url = 'https://i.nhentai.net/galleries/'+ str(m) +'/'
        match = re.search(r'\d+', prefix_url)
        if match:
            webname = str(m)
        else:
            print('No match found')
        os.makedirs(BookPath + '/' + webname + '/', exist_ok=True)

        thumb_file_path = BookPath + '/' + webname + '/thumb.png'
        thumb_picture_url = prefix_url + 'thumb.png'
        # download(thumb_file_path, thumb_picture_url)

        n = 1000
        prev_sizes = [None, None, None]  # Store the sizes of the last three images
        for i in range(1, n + 1):
            file_path = BookPath + '/' + webname + '/' + str(i) + '.png'
            picture_url = prefix_url + str(i) + '.png'
            download(file_path, picture_url)

            # Update the list with the size of the new image
            if i >= 3:
                prev_sizes.pop(0)
                prev_sizes.append(os.path.getsize(file_path))

                # If the last three sizes are the same, stop downloading and delete the last three images
                if prev_sizes[0] == prev_sizes[1] == prev_sizes[2]:
                    print(f'Three consecutive images of the same size detected, stopping download!')
                    for j in range(3):
                        os.remove(BookPath + '/' + webname + '/' + str(i-j) + '.png')
                    break

if __name__ == '__main__':
    main()
