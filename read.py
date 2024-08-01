import os
import json

def index_folders(path):
    folder_dict = {}
    # 遍历当前路径下的所有文件和文件夹
    for entry in os.scandir(path):
        if entry.is_dir():
            # 递归调用以遍历子文件夹
            folder_dict[entry.name] = index_folders(entry.path)
    return folder_dict

# 设置当前工作目录
current_path = '.'
# 创建索引
folder_index = index_folders(current_path)

# 将索引写入JSON文件
with open('folder_index.json', 'w', encoding='utf-8') as f:
    json.dump(folder_index, f, ensure_ascii=False, indent=4)

print("索引已经创建并保存到 'folder_index.json' 文件中。")
