import subprocess
import os
from concurrent.futures import ThreadPoolExecutor


def run_script(script):
    process = subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    with open('log.txt', 'a') as log_file:
        if stdout:
            log_file.write(stdout.decode('utf-8'))
        if stderr:
            log_file.write(stderr.decode('utf-8'))


print("开始下载进程")
path = "./Book"
os.makedirs(path, exist_ok=True)

scripts = ["./GetBook/Get_Book_1_jpg.py", "./GetBook/Get_Book_2_jpg.py", "./GetBook/Get_Book_3_jpg.py"]

with ThreadPoolExecutor() as executor:
    executor.map(run_script, scripts)

print("下载完成")
