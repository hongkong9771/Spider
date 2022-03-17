# -*- coding : utf-8 -*- 
# @Time : 2020/11/20 14:56
# @Author : 危红康
# @File : spider_version3.py
# @Software: PyCharm

"""
    此版本用于下载所有文件，并且可以根据年月份进行分类管理，自动创建相应的文件夹，若文件夹已存在，则跳过；
    在下载图片时，若图片已存在，则跳过，若不存在，则继续下载，相较于前面两个version，此版本有很大的提升。
    在下载过程中如若出现下载错误，可能有以下几个原因：
    1.网络状态不佳；
    2.headers缺少cookie或者Referer信息；
    3.短时间内多次访问该网址，被服务器远程断连，因此，在下载过程中需要加一个延时，避免过快过频繁的访问；
"""

import requests
import parsel
from tqdm import tqdm
import os
import time


def main():
    baseurl = "https://www.vmgirls.com/archives.html"
    head = {
        "User-Agent": "Your User-Agent information",
        "cookie": "Your cookie information"
    }
    name_year, name_month, number_year, number_month = file_path_name(baseurl, head)
    html = askurl(baseurl, head)
    names, urls = getlinks(html)        # 所有专辑的名字和链接
    # print(len(urls))
    '''
    可以设置从断点处下载，更改下面month_index和urls_index的值。
    当专辑下载断连时，需要考虑sum_month的值，，在跳转年份文件夹时，需要重新初始化为0；
    month_index：月份链接索引，从0开始
    urls_index：专辑链接索引，从0开始
    二者必须匹配
    '''
    month_index = 0     # 月份链接索引
    urls_index = 0    # 专辑链接索引
    j = 0
    for i in range(len(number_year)):
        # print(name_year[i])     # 每个年份的名字（用作文件夹名）
        sum_month = 0
        month_index += j        # 每年的月份个数（累加）
        # print(month_index)
        # if i == 0 or i == 1 or i == 2 or i == 3:      # 跳过2020、2019、2018、2017年的下载（根据下载需要进行设置 ）
        #     continue
        for j in range(len(number_month[month_index:])):
            each_month = int(number_month[j + month_index])     # 每个月的专辑数
            sum_month += each_month                             # 每个月的专辑数累加
            # print(name_month[j + month_index], end=' ')         # 每个月份的名字（用作文件夹名）
            # print(urls[urls_index:(urls_index + each_month)])   # 每个月的专辑链接
            # print(urls_index)
            for url in tqdm(urls[urls_index:(urls_index + each_month)]):    # 按每个月来下载（遍历每个月的专辑数）
                index = urls.index(url)
                print("  正在下载第", index + 1, "个专辑：", names[index])
                createdir(name_year[i], name_month[j+month_index], names[index])
                url = "https://www.vmgirls.com/" + url
                # print(url)
                pictures_urls = get_pic_links(url, head)
                # print(pictures_urls)
                download(name_year[i], name_month[j+month_index], names[index], pictures_urls, head)
                print(names[index] + " " + "下载成功！")
                time.sleep(15)
            urls_index += each_month
            if sum_month == int(number_year[i]):
                j += 1
                # print('\n')
                break


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
    links1 = parse.xpath('//div[@class="nc-light-gallery"]/a/img/@data-src').getall()       # 匹配大部分专辑图片
    links2 = parse.xpath('//div[@class="nc-light-gallery"]/p/a/img/@data-src').getall()     # 有少部分专辑图片因为多加了一个p标签而无法匹配
    links3 = parse.xpath('//div[@class="nc-light-gallery"]/figure/ul/li/figure/a/img/@data-src').getall()  # 同上
    links4 = parse.xpath('//div[@class="nc-light-gallery"]/img/@data-src').getall()         # 有少部分专辑图片没有a标签
    links5 = parse.xpath('//div[@class="nc-light-gallery"]/p/img/@data-src').getall()
    links = links1 + links2 + links3 + links4 + links5
    # print(links)
    return links


# 为每个专辑创建一个文件夹，每个专辑存放在对应的年份和月份文件夹中
# 文件夹创建时只能一级一级的创建，不能一下子创建多级文件夹
def createdir(name_year, name_month, dir_name):
    if not os.path.exists(name_year):
        os.mkdir(name_year)
    if not os.path.exists(name_year + '/' + name_month):
        os.mkdir(name_year + '/' + name_month)
    if not os.path.exists(name_year + '/' + name_month + '/' + dir_name):
        os.mkdir(name_year + '/' + name_month + '/' + dir_name)


# 下载内容
def download(name_year, name_month, dir_name, urls, head):
    for url in urls:
        file_name = urls.index(url) + 1
        if not os.path.exists(name_year + '/' + name_month + '/' + dir_name + '/' + str(file_name) + ".jpg"):
            if "https:" not in url:
                url = "https:" + url
            response = requests.get(url, headers=head)
            with open(name_year + '/' + name_month + '/' + dir_name + '/' + str(file_name) + ".jpg", 'wb') as f:
                f.write(response.content)
                time.sleep(5)
            # print(file_name + "下载成功！")


# 提取年和月的文件夹名
def file_path_name(url, head):
    html = askurl(url, head)
    parse = parsel.Selector(html)
    name_year = parse.xpath('//h4/text()').getall()
    name_month = parse.xpath('//span[@class="al_mon"]//text()').getall()

    # 每年的专辑数量
    number_year = []
    for i in range(len(name_year)):
        number_year_former = name_year[i].index(name_year[i][6])
        number_year_latter = name_year[i].index(name_year[i][-1])
        year = name_year[i][number_year_former + 1:number_year_latter]
        number_year.append(year)
        # number_year = int(number_year)
    # print(number_year)

    #  每个月的专辑数量
    number_month = []
    for i in range(len(name_month)):
        number_month_former = name_month[i].index(name_month[i][5])
        number_month_latter = name_month[i].index(name_month[i][-1])
        month = name_month[i][number_month_former + 1:number_month_latter]
        number_month.append(month)
    #     number_month = int(number_month)
    # print(number_month)

    # print(name_year)
    # print(name_month)
    return name_year, name_month, number_year, number_month


if __name__ == "__main__":
    main()
    print("爬取完毕")
