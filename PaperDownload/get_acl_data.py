# -*- coding = utf-8 -*-
# 2023/5/15 16:09
import os

import requests
from bs4 import BeautifulSoup
import openpyxl
import re

folder_path = r'D:\files\pythonStudy\PythonProjects\download\naacl'

# 保存Excel文件
# workbook.save('output.xlsx')
xls_file = r'D:\files\pythonStudy\PythonProjects\download\output_naacl.xlsx'
xls = openpyxl.load_workbook(xls_file) # 打开 excel 文件
sheet = xls.worksheets[0] # 通过索引获取第 1 个表格中的内容，一个 excel 文件可能会包含多个表格
cnt = 0
for cnt in range(2, 137):
    print(cnt)
    new_title_id = str(sheet.cell(cnt,3).value).split('/')[-1]
    sss = "?paper_id="
    # acl
    # new_title_id = re.sub("\?paper_id=acl-","",new_title_id)
    # new_title_id = re.sub("-[0-9]{4}-[0-9]{2}-[0-9]{2}",'',new_title_id)

    # emnlp
    new_title_id = re.sub("\?paper_id=emnlp-","",new_title_id)
    new_title_id = re.sub("-[0-9]{4}-[0-9]{2}-[0-9]{2}",'',new_title_id)


    # naacl
    new_title_id = re.sub("\?paper_id=naacl-","",new_title_id)
    new_title_id = re.sub("-[0-9]{4}-[0-9]{2}-[0-9]{2}",'',new_title_id)

    # print(new_title_id)
    # https: // aclanthology.org / 2022.emnlp - main.759.pdf
    # https: // aclanthology.org / 2022.naacl - main.319.pdf
    download_url = "https://aclanthology.org/" + new_title_id + ".pdf"
    print(download_url)
    response = requests.get(download_url)
    if response.status_code == 200:
        file_name = os.path.join(folder_path, download_url.split('/')[-1])
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print("{name}PDF文件已成功下载到文件夹中".format(name=new_title_id))
    else:
        print("下载PDF文件失败")
