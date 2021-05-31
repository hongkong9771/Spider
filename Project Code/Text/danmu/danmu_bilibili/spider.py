# -*- coding : utf-8 -*- 
# @Time : 2020/10/13 15:31
# @Author : 危红康
# @File : spider.py
# @Software: PyCharm


import requests
import parsel
import xlwt

def main():
    baseurl = "https://api.bilibili.com/x/v2/dm/history?type=1&oid=245944145&date=2020-10-22"
    datalist = getdata(baseurl)
    savepath = "B站弹幕.xls"
    # 保存数据
    savedata(datalist, savepath)


# 解析网页并爬取数据
def getdata(baseurl):
    html = askurl(baseurl)
    parse = parsel.Selector(html)          # 解析html网页
    datalist = parse.xpath("//d/text()").getall()
    # print(datalist)
    return datalist


def askurl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "cookie": "_uuid=E863ABB5-4C64-0AE1-83DF-004FC306502D02430infoc; buvid3=F744E38F-0A3D-406B-B69E-4D503072EC4D53934infoc; LIVE_BUVID=AUTO4515853072416665; rpdid=|(k)~uYmYukk0J'ul)lJ|~kRR; sid=jkd9o508; DedeUserID=308237050; DedeUserID__ckMd5=97a92453947d3843; SESSDATA=ce680807%2C1610097505%2C11007*71; bili_jct=14641e02251be2d5da1ab290a8c42f0b; CURRENT_FNVAL=80; blackside_state=1; PVID=1; bfe_id=cade757b9d3229a3973a5d4e9161f3bc"
    }
    response = requests.get(url=url, headers=head)
    html = response.content.decode("utf-8")
    """
    或者这样写也可以，两种写法都可以获得同样的网页信息
    response.encoding = 'utf-8'
    html = response.text
    """
    # print(html)
    return html


def savedata(datalist, savepath):
    print('saving...')
    danmu = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = danmu.add_sheet('B站弹幕', cell_overwrite_ok=True)  # 创建工作表
    col = ['序号', '弹幕']
    for i in range(0, 2):
        sheet.write(0, i, col[i])

    for i in range(len(datalist)):
        sheet.write(i + 1, 0, i+1)    # 序号写入
        sheet.write(i + 1, 1, datalist[i])    # 数据写入

    danmu.save(savepath)                      # 保存数据表


if __name__ == "__main__":
    main()
    print('弹幕爬取完毕')
