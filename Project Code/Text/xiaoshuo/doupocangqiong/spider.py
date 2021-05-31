# -*- coding : utf-8 -*- 
# @Time : 2020/10/20 20:56
# @Author : 危红康
# @File : spider.py
# @Software: PyCharm


import requests
from bs4 import BeautifulSoup
import parsel
from tqdm import trange


def main():
    source_url = "https://www.xsbiquge.com"
    url = "https://www.xsbiquge.com/1_1413/"
    book_name = "斗破苍穹.txt"
    # if not os.path.exists(book_name):
    #     os.mkdir(book_name)
    html = askurl(url)
    links, names = getlink(html, source_url)
    # print(links)
    # print(names)
    for i in trange(len(links)):
        html = askurl(links[i])
        chapter_name = names[i]     # 章节名
        # print(links[i])
        # print(chapter_name)
        chapter_content = getdata(html)
        with open(book_name, 'a', encoding='utf-8') as f:
            f.write(chapter_name)
            f.write('\n'*2)
            f.write('\n'.join(chapter_content))
            f.write('\n'*3)


def askurl(url):
    response = requests.get(url=url)
    response.encoding = "utf-8"
    html = response.text
    # print(html)
    return html


def getlink(html, source_url):
    chapters_link = []
    chapters_name = []
    parse = parsel.Selector(html)
    links = parse.xpath('//dd/a/@href').getall()
    names = parse.xpath('//dd/a/text()').getall()
    for link in links:
        link = source_url + link
        chapters_link.append(link)
    # print(datas)
    for name in names:
        chapters_name.append(name)
    return chapters_link, chapters_name


def getdata(html):
    soup = BeautifulSoup(html, "html.parser")
    texts = soup.find("div", id="content")
    content = texts.text.strip().split('\xa0'*4)
    """
    使用text提取所有文字，使用strip方法去掉回车，
    最后使用split方法根据\xa0切分数据，因为每一段的开头都有四个空格
    最后的content以每段为单位，储存为列表。
    """
    # print(content)
    return content


if __name__ == '__main__':
    main()
