# -*- coding : utf-8 -*- 
# @Time : 2020/10/28 13:40
# @Author : 危红康
# @File : spider.py
# @Software: PyCharm


import requests
import parsel
import os


def main():
    baseurl = "http://district.ce.cn/zg/201801/31/t20180131_27986901.shtml"
    # baseurl = "http://district.ce.cn/zg/201801/31/t20180131_27986752.shtml"
    # baseurl = "http://district.ce.cn/newarea/roll/201802/02/t20180202_28027386.shtml"

    links_time, file_names = getlink_time(baseurl)           # 此处只需提取年份的链接和年份名，titles不需要提取
    for i in range(0, 1):
    # for i in range(len(links_time)):
        # print(links_time[i])
        file_name = createdir(file_names[i])
        links_chapter, titles = getlink_title(links_time[i])    # 此处只需提取title链接和title名字，文件名不需要提取
        # for j in range(0, 1):
        for j in range(len(links_chapter)):
            print(titles[j], end=' ')
            print(links_chapter[j])

            contents = getdata(links_chapter[j])
            title = titles[j]+'.txt'
            with open(file_name + '/' + title, 'a', encoding='utf-8') as f:
                for content in contents:
                    f.write(content)
                    f.write('\n')


def askurl(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 85.0.4183.121Safari / 537.36",
        "Cookie": "ALLYESID4=145C392C5E235FF7; wdcid=06bbe0aa37294be7; zycna=bbZgbJbcYBQBATtH8ERoDVQv; Hm_lvt_d130ad2e0466d0dbb676e389eb463ef5=1603863475,1603969803,1604021031; wdses=1de1841d41e06a48; Hm_lpvt_d130ad2e0466d0dbb676e389eb463ef5=1604021726; wdlast=1604021735"

    }
    response = requests.get(url=url, headers=head)
    html = response.content.decode('gb18030')        # 需要根据编码格式来选择，可以查看网页meta标签下的charset属性值来确定编解码方式
    # response.encoding = "gb2312"
    # html = response.text
    # print(html)
    return html


def getlink_time(url):
    html = askurl(url)
    parse = parsel.Selector(html)
    links = parse.xpath('//p/a/@href').getall()
    file_names = parse.xpath('//p/a/font/strong/text()').getall()
    # print(links)
    # print(file_names)
    return links, file_names


def getlink_title(url):
    html = askurl(url)
    parse = parsel.Selector(html)
    links_1 = parse.xpath('//p/font[@color="#808080"]/strong/a/@href').getall()
    titles_1 = parse.xpath('//p/font[@color="#808080"]/strong/a/font[@color="#0000ff"]/text()').getall()
    # titles_1 = parse.xpath('//a/strong/font[@color="#0000ff"]/text()').getall()
    links_2 = parse.xpath('//p/a/@href').getall()
    titles_2 = parse.xpath('//font[@color="#3366ff"]/text()').getall()

    repeat = [i for i in links_1 if i in links_2]
    if len(repeat):
        for i in range(len(repeat)):
            links_2.remove(repeat[i])
    """
            当links_2中的链接已经出现在links_1中时，删除掉links_2中的重复链接。
    """
    # print(links_2)
    links = links_1 + links_2
    titles = titles_1 + titles_2
    '''
    使用正则表达式提取
    # links = []
    # titles = []
    # soup = BeautifulSoup(html, 'html.parser')
    # findLink = re.compile(r'href="(.*?)"')
    # for item in soup.find_all('a', target="_blank"):
    #     item = str(item)
    #     # print(item)
    #     link = re.findall(item, findLink)[0]
    #     links.append(link)
    '''
    # print(links)
    # print(titles)
    # print(links_1)

    # print(titles_2)
    return links, titles
    # return links_1, titles_1
    # return links_2, titles_2


def getdata(url):
    html = askurl(url)
    parse = parsel.Selector(html)
    texts = parse.xpath('//p/text()').getall()
    # print(texts)
    return texts


def createdir(title):
    dir_name = title
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    return dir_name


if __name__ == '__main__':
    main()
    print('爬取完毕！！！')
