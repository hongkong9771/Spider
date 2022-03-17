# -*- coding : utf-8 -*- 
# @Time : 2020/10/16 16:35
# @Author : 危红康
# @File : spider_version1.py
# @Software: PyCharm

"""
    此版本为网页首页直接下载，不包含所有专辑文件，不能按年月分类管理。

"""

import requests  # 请求网页
import re        # 正则表达式，匹配信息
from bs4 import BeautifulSoup       # 分析网页信息
import os        # 下载模块
import time
import parsel


def main():
    """
    利用head1本来就可以用于爬取下载页面，但是在下载过程中会遇到服务器连接失败等情况，
    可能是服务器自动断掉了连接，因此在下载的请求头中，封装了"accept"和"cookie"等信息（head2），
    以免被服务器识别为恶意下载。如果下载一部分之后，依然出现连接失败的话，可以考虑从断掉的地方接着下载。
    """
    head1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
    head2 = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Your User-Agent information",
        "cookie": "Your cookie information"
    }
    baseurl = "https://www.vmgirls.com/"
    html = askurl(baseurl, head1)
    urls = getlink(html)
    for url in urls:       # 若下载中途失败，可以在此处从断联处开始接着下载
        html = askurl(url, head1)
        dir_name = createdir(html)
        datalist = getdata(html)
        # print(datalist)
        p = urls.index(url)     # 定位到断联处
        print("%d" % (p+1), end=" ")
        print("正在下载 " + dir_name + " ...")
        print(url)
        download(datalist, dir_name, head2)
        print(dir_name + " 下载成功!")


def askurl(url, head):
    response = requests.get(url, headers=head)
    html = response.text
    # print(html)
    return html


# 解析网页，获取到所有页面的URL
def getlink(html):
    datas = []
    parse = parsel.Selector(html)
    links = parse.xpath('//a[@class="media-content"]/@href').getall()
    # print(links)
    for link in links:
        newlink = "https://www.vmgirls.com/" + link
        if newlink not in datas:
            datas.append(newlink)
    # print(datas)
    return datas


# 解析网页，获取该页面的所有图片链接
def getdata(html):
    datalist = []
    soup = BeautifulSoup(html, "html.parser")
    findImgsrc = re.compile(r'data-src="(.*?)"')
    for item in soup.find_all("img", class_="size-full"):
        # print(item)
        item = str(item)
        link = re.findall(findImgsrc, item)[0]
        # print(link)
        datalist.append("https://www.vmgirls.com/" + link)
    for item in re.findall('<a href="(.*?)" alt=".*?" title=".*?"', html):
        # print(item)
        datalist.append("https://www.vmgirls.com/" + item)
    # print(datalist)
    return datalist


# 创建文件夹名称
def createdir(html):
    dir_name = re.findall(r'<h1 class="post-title h1">(.*?)</h1>', html)[0]
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    # print(dir_name)
    return dir_name


# 下载图片
def download(datalist, dir_name, head):
    for data in datalist:
        time.sleep(0.5)  # 推迟调用线程（此处为推迟0.25S）
        file_name = data.split("/")[-1]
        response = requests.get(data, headers=head)
        with open(dir_name + '/' + file_name, 'wb') as f:
            f.write(response.content)
            # print(file_name + "下载成功")


if __name__ == "__main__":
    main()
    print("下载完毕")