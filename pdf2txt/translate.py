# -*- coding = utf-8 -*-
# 2023/4/27 12:51
import hashlib
import time
import requests
import os
import json


# 将英文文本翻译为中文文本
def translate(text):
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    # appid = '20230427001657968'  # 在百度翻译 API 上申请的 App ID
    appid = '20230427001658751'  # 在百度翻译 API 上申请的 App ID
    secret = 'zgtj1CbXG5InfbaCDwu7'  # 在百度翻译 API 上申请的密钥
    # secret = '6jQvc6IbqHYnnPcep3R9'  # 在百度翻译 API 上申请的密钥
    params = {
        'q': text,
        'from': 'en',
        'to': 'zh',
        'appid': appid,
        'salt': '123456',
        'sign': hashlib.md5((appid + text + '123456' + secret).encode('utf-8')).hexdigest()
    }
    response = requests.get(url, params=params)
    content = response.content.decode('utf-8')
    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        print(f'JSONDecodeError: {e.msg} - line {e.lineno} column {e.colno}')
        # 处理JSON格式错误
        return None
    result = response.json()
    if result.get('error_code') is None:
        return result['trans_result'][0]['dst']
    else:
        return None


def trans_file(source_file, target_file):
    queue = []  # 待翻译队列
    with open(source_file, 'r', encoding='utf-8') as f1, open(target_file, 'w', encoding='utf-8') as f2:
        for i, line in enumerate(f1):
            queue.append((i, line.strip()))

        while queue:
            i, text = queue.pop(0)
            result = translate(text)
            if result:
                f2.write(f"{i}\t{result}\n")
            else:
                queue.append((i, text))
                time.sleep(0.1)  # 等待后重试


def sort_(source_file, target_file):
    # 读取目标文件并按照原始行号排序
    lines = []
    with open(source_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().split('\t')
            lines.append((int(line[0]), line[1]))
        lines.sort(key=lambda x: x[0])

    # 写入新文件
    with open(target_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line[1] + '\n')


def deal_all_file(fileindir, fileoutdir, filemiddir):
    for filename in os.listdir(fileindir):
        source_file = os.path.join(fileindir, filename)
        # 读取源文件并进行翻译
        target_file = os.path.join(filemiddir, filename)
        sort_file = os.path.join(fileoutdir, filename)
        trans_file(source_file, target_file)
        sort_(target_file, sort_file)


# def read_file(fileindir, fileoutdir):


if __name__ == '__main__':
    # 读取源文件并进行翻译
    deal_all_file("./txt/", "./translate/", "./translate_/")
    # source_file = "./txt/AlephBERT_Language Model Pre-training and Evaluation from Sub-Word to Sentence Level.txt"
    # # 读取源文件并进行翻译
    # target_file = "./translate/AlephBERT_Language Model Pre-training and Evaluation from Sub-Word to Sentence Level.txt"
    # sort_file = "./translate_/AlephBERT_Language Model Pre-training and Evaluation from Sub-Word to Sentence Level.txt"
    # trans_file(source_file, target_file)
    # sort_(target_file, sort_file)