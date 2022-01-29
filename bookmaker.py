import os
import re
import shutil
from time import sleep
from winsound import Beep

import pylatex
import requests
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


def write_files(contents, title):
    i = 0
    for link in contents:
        file_name = title + str(i)+'.tex'
        print('开始下载第', i, '章')
        resp_chapter = safe_request(link)
        text_chapter = resp_chapter.text
        parse_chapter = etree.HTML(text_chapter)
        origin_name = parse_chapter.xpath('//h1/text()')[0]
        print(origin_name)
        chapter_name = latexize_str(origin_name)
        blank = False  # 非正式章节
        if not re.search(r"第.*?章", chapter_name):
            print("跳过非正式章节")
            blank = True

        with open(file_name, 'w', encoding='UTF-8-sig') as chapter:
            if blank == True:
                chapter.write("",)
            else:
                chapter.write(
                    r"\chapter{"+re.sub(r"第.*?章", "", chapter_name)+'}\n')
                p_list = parse_chapter.xpath('//*[@id="content"]/p/text()')
                for p in p_list:
                    if "最新网址" in p or "，"+title in p or re.search(r"第.*?章", p):
                        print("删除了广告", p)
                        continue
                    chapter.write(latexize_str(p)+'\n\n')
        i = i + 1


def safe_request(link):
    status = 0
    j = 0
    while status != 200:
        try:
            resp = requests.get(link, headers=headers, timeout=2)
        except:
            status = 1
        else:
            status = resp.status_code
        if j >= 1:
            sleep(0.5)
            print("请求出错，正在重试。")
        j = j + 1
    return resp


def latexize_str(str):
    tmpdoc = pylatex.Document()
    tmpdoc.append(str)
    uncutstr = tmpdoc.dumps()
    uncutstr = uncutstr.replace(
        '\\documentclass{article}%\n\\usepackage[T1]{fontenc}%\n\\usepackage[utf8]{inputenc}%\n\\usepackage{lmodern}%\n\\usepackage{textcomp}%\n\\usepackage{lastpage}%\n%\n%\n%\n\\begin{document}%\n\\normalsize%\n', '')
    return uncutstr.replace("%\n\\end{document}", "")


def main(contents_url):
    texbody = r'''\documentclass{ctexbook}
\usepackage{geometry}
\usepackage{hyperref}
\geometry{a4paper,scale=0.8}
\begin{document}
\title{TITLE}
\author{AUTHOR}
\date{}
\maketitle
\tableofcontents
\input{lists}
\end{document}
    '''
    # contents_url = input("需要目录的链接。\n")
    # contents_url = 'http://www.b5200.net/52_52542/'
    # 请求目录
    sign_of_timeout = True
    resp_contents = safe_request(contents_url)
    print("已经请求目录。")
    text_contents = resp_contents.text
    et_contents = etree.HTML(text_contents)
    contents = et_contents.xpath('//*[@id="list"]/dl/dd/a/@href')[9:]
# gen摘要
    shutil.rmtree("work", ignore_errors=True)  # 最好手动删除临时目录
    try:
        os.mkdir('work')
    except:
        pass
    os.chdir("work")
    title = et_contents.xpath("//h1/text()")[0]
    print("标题：", title)
# 获取作者
    origin_author = et_contents.xpath('//*[@id="info"]/p[1]/text()')[0]
    author = re.sub(r"作.*?者：", "", origin_author)
    print("作者：", author)
    texbody = re.sub(r"TITLE", latexize_str(title), texbody)
    texbody = re.sub(r"lists", latexize_str(title) + "lists", texbody)
    texbody = re.sub(r"AUTHOR", latexize_str(author), texbody)
# 写入摘要
    with open(title + 'output.tex', 'w', encoding='UTF-8') as output:
        output.write(texbody)
    with open(title + "lists.tex", 'w', encoding='UTF-8') as lists:
        i = 0
        for content in contents:
            lists.write('\\input{' + title + str(i) + '}' + '\n')
            i = i + 1
# 写入内容文件
    write_files(contents, title)
# 编译
    os.system("xelatex -synctex=1 -interaction=nonstopmode " +
              title + "output.tex")
    os.system("xelatex -synctex=1 -interaction=nonstopmode " +
              title + "output.tex")
    os.system("pandoc "+title+'output.tex'+' -o '+ title+'output.epub')
    os.chdir("..")
    shutil.copyfile('./work/' + title + 'output.epub',title + '.epub')
    shutil.copyfile("./work/" + title + "output.pdf", title + ".pdf")
    print(title, '已经编译成功，正在播放提示音……')
    Beep(440, 2000)


links = []
try:
    with open("links.txt", 'r') as links_txt:
        for link in links_txt:
            if 'http' in link:
                links.append(link)
except FileNotFoundError:
    print("请编辑links.txt")
    exit()
for link in links:
    main(link)
