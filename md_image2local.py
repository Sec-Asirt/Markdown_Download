import misaka
import os
import requests
from bs4 import BeautifulSoup
import sys
import re
import argparse
import time

# 创建一个空字典来保存URL和文件名
url_to_filename = {}

# 参数解析
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', help="markdown directory")
    parser.add_argument('--modify_source', action='store_true', help="whether to modify source md file directly")
    parser.add_argument('--absolute_path', action='store_true', help="Modify in absolute address mode")

    return parser.parse_args()

# 遍历所有文件
def get_files_list(dir):
    """
    topdown=False 获取一个目录下所有文件列表，包括子目录
    :param dir:
    :return:
    """
    files_list = []
    extension = '.md'
    #for root, dirs, files in os.walk(dir, topdown=False):
    for root, dirs, files in os.walk(dir):
        for file in files:
            # 检查文件后缀
            if file.endswith(extension):
                files_list.append(os.path.join(root, file))

    return files_list

# 获取文件中图片链接
def get_pics_list(md_content):
    """
    获取一个markdown文档里的所有图片链接
    :param md_content:
    :return:
    """
    md_render = misaka.Markdown(misaka.HtmlRenderer())
    html = md_render(md_content)
    soup = BeautifulSoup(html, features='html.parser')
    pics_list = []
    for img in soup.find_all('img'):
        pics_list.append(img.get('src'))
    
    return pics_list

# 下载资源
def download_pics(url, file) -> int:
    # 文件所在路径
    dirname = os.path.dirname(file)
    # 获取文件名
    filename = os.path.basename(file)
    # 拼接文件名
    targer_dir = os.path.join(dirname, f'{filename}.assets')

    # 如果目录不存在则创建
    if not os.path.exists(targer_dir):
        os.mkdir(targer_dir)
    
    # 使用正则表达式匹配文件名
    match = re.search(r'/([^/]*\.(?:png|jpg|jpeg|gif|bmp))', url)
    if not match:
        return 1
    
    #过滤非法字符串
    Filter_string = re.sub(r"[^a-zA-Z0-9\n\.]", "", match.group(1))

    # 检查文件是否存在, 存在则返回
    file_path = targer_dir + '\\' + Filter_string
    if os.path.exists(file_path):
        return 2

    # https请求
    img_data = requests.get(url).content

    # 声明全局变量
    global url_to_filename

    # 保存到全局字典
    url_to_filename[url] =  Filter_string

    # 保存到文件
    with open(os.path.join(targer_dir, Filter_string), 'w+') as f:
        f.buffer.write(img_data)

    return 0

# 替换url
def file_replace_url(file_data: str, targer_dir: str) -> str:
    
    for key, value in url_to_filename.items():
        file_data = file_data.replace(key, targer_dir + value)

    return file_data

# 写入文件
def write_file(folder_path: str, file_name: str, file_data: str):
    with open(os.path.join(folder_path, file_name), "w", encoding="utf-8") as file:
        file.write(file_data)

# 进度条
def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    sys.stdout.write(f'\r[-] Downloading ({progress}/{total})|{bar}|{percent:.2f}%')
    sys.stdout.flush()

# 主函数
def main():

    # 获取参数
    args = parse_args()
    # 如果路径为空则退出
    if not args.path:
        print("[-]Please add md_path arg and rerun this file...")
        return

    # 遍历文件夹下的所有.md文档
    files_list = get_files_list(args.path)
    # 遍历目录下的文件
    for file in files_list:
        print(f'[+] Processing... {file}')
        # 打开文件并读取
        with open(file, encoding='utf-8') as f:
            md_content = f.read()
        # 获取文件中的图片链接
        pics_list = get_pics_list(md_content)
        print(f'[-] Discover images {len(pics_list)} sheet')
        # 下载所有图片
        for index, pic in enumerate(pics_list):
            status = download_pics(pic, file)
            progress_bar(index + 1, len(pics_list))
        #print()
        # 判断是否需要替换
        if args.modify_source:
            dirname=".\\"
            # 判断是否以绝对路径的方式替换
            if args.absolute_path:
                dirname = os.path.dirname(file)
            # 拼接路径
            filename = os.path.basename(file)
            targer_dir = os.path.join(dirname, f'{filename}.assets\\')
            # 替换理解
            file_data = file_replace_url(md_content, targer_dir)
            # 将替换后的数据写入文件
            write_file(args.path, file, file_data)
            print(f'\n[+] Completed successfully')



if __name__ == '__main__':
    main()