# -*- coding : utf-8 -*- 
# @Time : 2020/11/11 19:15
# @Author : whk
# @File : spider_version2.py
# @Software: PyCharm

"""
    此版本用于下载所有专辑文件，可以在for循环内更改下载的范围；
    但是无法根据年份和月份进行分类管理，即无法按多个文件夹进行分类
"""

import requests
import parsel
from tqdm import tqdm, trange
import os


def main():
    baseurl = "https://www.vmgirls.com/archives.html"
    head = {
        "User-Agent": "Your User-Agent information",
        "cookie": "Your cookie information"
    }
    html = askurl(baseurl, head)
    names, urls = getlinks(html)        # 所有专辑的链接
    for url in tqdm(urls[7:83]):        # 在此处调节专辑的范围
        print("正在下载第", index + 1, "个专辑：", names[index])
        index = urls.index(url)
        dir_name = createdir(names[index])
        url = "https://www.vmgirls.com/" + url
        # print(url)
        pictures_urls = get_pic_links(url, head)
        # print(pictures_urls)
        download(dir_name, pictures_urls, head)
        # print(dir_name + " " + "下载成功！")


# 获取网页
def askurl(url, head):
    response = requests.get(url, headers=head)
    html = response.text
    # print(html)
    return html


# 解析网页，获取页面所有专辑链接和专辑名
def getlinks(html):
    parse = parsel.Selector(html)
    names = parse.xpath('//ul[@class="al_mon_list"]/li/ul/li/a/text()').getall()
    links = parse.xpath('//ul[@class="al_mon_list"]/li/ul/li/a/@href').getall()
    # print(names)
    return names, links


# 解析网页，获取单个专辑链接的所有图片链接
def get_pic_links(url, head):
    html = askurl(url, head)
    parse = parsel.Selector(html)
    links = parse.xpath('//div[@class="nc-light-gallery"]/a/img/@data-src').getall()
    return links


# 为每个专辑创建一个文件夹
def createdir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    return dir_name


# 下载内容
def download(dir_name, urls, head):
    for url in urls:
        file_name = urls.index(url) + 1
        url = "https:" + url
        response = requests.get(url, headers=head)
        with open(dir_name + '/' + str(file_name) + ".jpg", 'wb') as f:
            f.write(response.content)
            # print(file_name + "下载成功！")


if __name__ == "__main__":
    main()
    print("爬取完毕")
