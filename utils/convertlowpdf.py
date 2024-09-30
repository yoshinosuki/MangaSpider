import os
from PIL import Image, UnidentifiedImageError, ImageFile
import re
import gc
import datetime
import shutil

ImageFile.LOAD_TRUNCATED_IMAGES = True

base_folder_paths = [r'..\book', ]
downloadPdfPath = r'..\book'
temp_folder = r'..\book\temp'
quality = 20  # 质量参数，范围从1（最差）到95（最好）


def degrade_images_in_folder(input_folder, output_folder, quality):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 打开原始图片
            image = Image.open(input_path)

            # 保存图片，设置质量参数
            image.save(output_path, quality=quality)
            print(f"Processed {filename}")


def jpgs_to_pdf(folder_path, error_log):
    folder_name = os.path.basename(folder_path)
    temp_folder_path = os.path.join(temp_folder, folder_name)

    # 压缩图片并保存到临时文件夹
    degrade_images_in_folder(folder_path, temp_folder_path, quality)

    # 获取所有文件
    jpg_files = [f for f in os.listdir(temp_folder_path) if f.lower().endswith(('.jpg', '.png'))]

    # 按文件名中的数字排序
    def extract_number(filename):
        numbers = re.findall(r'\d+', filename)
        if numbers:
            return int(''.join(numbers))
        return 0

    jpg_files.sort(key=extract_number)

    images = []

    for f in jpg_files:
        try:
            img = Image.open(os.path.join(temp_folder_path, f))
            images.append(img)
        except (UnidentifiedImageError, OSError) as e:
            error_message = f"无法打开文件: {f}, 错误: {e}"
            error_log.append(error_message)
            print(error_message)

    # 保存为PDF
    if images:
        pdf_path = os.path.join(downloadPdfPath, f"{folder_name}.pdf")
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"PDF文件已保存到: {pdf_path}")
    else:
        print("没有找到图片文件")

    # 清理内存
    for img in images:
        img.close()
    images.clear()
    gc.collect()


def clear_temp_folder(temp_folder):
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
        print(f"临时文件夹已清除: {temp_folder}")


def convert_all_folders(base_folder_paths):
    error_log = []

    for base_folder_path in base_folder_paths:
        if not os.path.exists(base_folder_path):
            print(f"路径不存在: {base_folder_path}")
            continue

        # 获取所有子文件夹
        subfolders = [f.path for f in os.scandir(base_folder_path) if f.is_dir()]

        for folder in subfolders:
            jpgs_to_pdf(folder, error_log)

    if error_log:
        # 获取当前时间并格式化为字符串
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"error_log_{current_time}.txt"
        log_path = os.path.join(base_folder_paths[0], log_filename)

        with open(log_path, 'a') as log_file:
            for error in error_log:
                log_file.write(f"{error}\n")
        print(f"错误日志已保存到: {log_path}")

    # 清除临时文件夹
    clear_temp_folder(temp_folder)


# 实例化
convert_all_folders(base_folder_paths)
