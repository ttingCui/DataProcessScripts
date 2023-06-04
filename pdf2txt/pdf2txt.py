import PyPDF2
import re
import os


def pdf2txt(filein, fileout):
    # 打开PDF文件
    pdf_file = open(filein, 'rb')
    # 创建一个PDF阅读器对象
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # 获取PDF文件的页数
    num_pages = len(pdf_reader.pages)
    # 遍历每一页，将文本内容添加到字符串中
    text = ''
    for i in range(num_pages):
        # 获取页面对象
        page = pdf_reader.pages[i]
        # 获取页面内容
        page_content = page.extract_text()

        # 从论文标题开始之前的内容全部舍弃
        # 使用basename()函数获取文件名字符串
        title = os.path.basename(filein)
        title = re.match(r'\b\w+\b', title).group()
        title = title.replace("_", " : ")
        if title in page_content:
            index = page_content.index(title)
            page_content = page_content[index:]

        #如果含有参考文献则只添加参考文献之前的信息
        if 'References'in page_content or 'REFERENCES' in page_content:
           if 'References'in page_content:
                index = page_content.index('References')
                before_str = page_content[:index]
                text += before_str
                text = re.sub(r'\n', ' ', text)
                text = re.sub(r'(?<=[.!?])\s+', '\n', text)
                text = re.sub(r'- ', '', text)
                break
           else:
               index = page_content.index('REFERENCES')
               before_str = page_content[:index]
               text += before_str
               text = re.sub(r'\n', ' ', text)
               text = re.sub(r'(?<=[.!?])\s+', '\n', text)
               text = re.sub(r'- ', '', text)
               break

        text += page_content

        text = re.sub(r'\n', ' ', text)

        text = re.sub(r'(?<=[.!?])\s+', '\n', text)
        text = re.sub(r'- ', '', text)
    # 摘要部分处理
    match = re.search(r"Abstract", text)
    if match:
        # 如果找到了 Abstract，就将该行句子拆成两行，并用新的字符串替换原始数据中的该行
        abstract_line_start = match.start()  # 找到该行句子的开头
        abstract_line_middle = match.start() + len("Abstract ")  # 找到该行句子的开头
        abstract_line_end = text.find("\n", match.end())  # 找到该行句子的结尾
        first_part = text[:abstract_line_start] + "\n"
        second_part = text[abstract_line_start:abstract_line_middle] + "\n"
        text = first_part + second_part + text[abstract_line_middle:abstract_line_end] + text[abstract_line_end:]

        # text = re.sub(r'Abstract', '\nAbstract', text)
    # 将文本保存为TXT文件
    with open(fileout, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
    # 关闭PDF文件
    pdf_file.close()

def dealfile(fileindir, fileoutdir):
    for filename in os.listdir(fileindir):
        path = os.path.join(fileindir, filename)
        pdf2txt(path, fileoutdir+"/"+filename.rstrip('.pdf')+".txt")

if __name__ == '__main__':
    dealfile("./data", "./txt")
    # pdf2txt("./data/AlephBERT_Language Model Pre-training and Evaluation from Sub-Word to Sentence Level.pdf", "test.txt")