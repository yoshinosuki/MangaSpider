import subprocess
import os
from concurrent.futures import ThreadPoolExecutor
import sys


def run_script(script):
    process = subprocess.Popen([sys.executable, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    with open('log.txt', 'a') as log_file:
        if stdout:
            log_file.write(stdout.decode('utf-8'))
        if stderr:
            log_file.write(stderr.decode('utf-8'))


print("开始下载进程")
path = "../book"
os.makedirs(path, exist_ok=True)

scripts = ["./tools/get_book_1.py", "./tools/get_book_2.py", "./tools/get_book_3.py"]

with ThreadPoolExecutor() as executor:
    executor.map(run_script, scripts)

print("下载完成，下载记录已保存")
