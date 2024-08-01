import subprocess
from datetime import datetime

# 定义文件路径
id_file_path = 'id.txt'
new_file_path = 'new.txt'
output_file_path = 'new_filtered.txt'


def read_file(file_path):
    """读取文件并返回每行内容组成的集合"""
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file if line.strip())


def write_file(file_path, data):
    """将数据写入文件"""
    with open(file_path, 'w') as file:
        for item in data:
            file.write(f"{item}\n")


def append_to_file(file_path, data):
    """将数据追加到文件"""
    with open(file_path, 'a') as file:
        for item in data:
            file.write(f"{item}\n")


def remove_duplicates(id_file, new_file, output_file):
    """移除new_file中在id_file中出现过的数字"""
    id_set = read_file(id_file)
    new_set = read_file(new_file)
    # 从new_set中移除在id_set中存在的项
    result_set = new_set - id_set
    write_file(output_file, result_set)


def read_numbers_from_file(filename):
    with open(filename, 'r') as file:
        numbers = file.read().splitlines()
        return [int(num) for num in numbers]


def write_numbers_to_file(filename, numbers):
    with open(filename, 'w') as file:
        for num in numbers:
            file.write(f"{num}\n")


def distribute_numbers(numbers):
    files = {1: [], 2: [], 3: []}
    length = len(numbers)
    # 按照顺序分配数字
    for i in range(length):
        files[(i % 3) + 1].append(numbers[i])
    # 将多余的数字分配给1.txt，但要先检查是否存在
    remainder = length % 3
    extra_numbers = []
    if remainder == 1:
        extra_numbers.append(numbers[-1])
    elif remainder == 2:
        extra_numbers.append(numbers[-2])
        extra_numbers.append(numbers[-1])
    for num in extra_numbers:
        if num in files[1]:
            files[1].remove(num)
    files[1].extend(extra_numbers)
    return files


def log_append_action(log_file, data):
    """记录追加操作到日志文件"""
    with open(log_file, 'a') as file:
        file.write(f"Appended on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n")
        for item in data:
            file.write(f"{item}\n")
            print(f"{item}\n")
        file.write("\n")


def log_append_action_notime(log_file, data):
    """记录追加操作到日志文件"""
    with open(log_file, 'a') as file:
        for item in data:
            file.write(f"{item}\n")
            print(f"{item}\n")
        file.write("\n")


def main():
    # 执行去重操作
    remove_duplicates(id_file_path, new_file_path, output_file_path)
    numbers = read_numbers_from_file(output_file_path)
    distributed_files = distribute_numbers(numbers)
    for i in range(1, 4):
        write_numbers_to_file(f'./GetBook/List/Target_{i}.txt', distributed_files[i])

    # 追加new_filtered.txt内容到id.txt并记录日志
    new_filtered_set = read_file(output_file_path)
    append_to_file(id_file_path, new_filtered_set)
    log_append_action('log.txt', new_filtered_set)


if __name__ == "__main__":
    main()
    print("分配任务完成")
    print("开始下载进程")
    scripts = ["./GetBook/Get_Book_1_jpg.py", "./GetBook/Get_Book_2_jpg.py", "./GetBook/Get_Book_3_jpg.py"]
    # 创建一个进程列表来保存每个脚本的进程
    processes = []
    # 启动每个脚本
    for script in scripts:
        process = subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)

    for process in processes:
        while True:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                print(output.decode('utf-8').strip())
                with open('log.txt', 'a') as log_file:
                    log_file.write(output.decode('utf-8'))

        # 获取错误输出
        stdout, stderr = process.communicate()
        if stderr:
            print(f"stderr: {stderr.decode('utf-8')}")
            with open('log.txt', 'a') as log_file:
                log_file.write(stderr.decode('utf-8'))


    print("下载完成")
