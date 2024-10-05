from PIL import Image
import os
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
# 将文件夹中的所有图片转换为JPG格式
input_folder = '../book'
output_folder = '../book'


def convert_to_jpg(input_path, output_path):
    # 打开图片
    img = Image.open(input_path)
    # 转换为RGB模式
    rgb_img = img.convert('RGB')
    # 保存为JPG格式
    rgb_img.save(output_path, format='JPEG')


if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.jpg'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        convert_to_jpg(input_path, output_path)
        print(f'Converted {filename} to JPG format.')

print('All images have been converted.')
