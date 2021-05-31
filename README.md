## Spider

始于2020.10.10

闲暇之际，爬虫自娱。



----

### 0.分类目录

----

本系列按照所爬取内容的格式，共分为以下几种：

| 内容    | 项目名称（代码链接）                                         | CSDN详解链接                                                 |
| ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Text    | [B站视频弹幕+词云分析](https://github.com/hongkong9771/Spider/tree/main/Project%20Code/Text/danmu/danmu_bilibili) | [B站视频弹幕+词云分析](https://blog.csdn.net/qq_41447478/article/details/117416669) |
| Picture | [唯美图片下载](https://github.com/hongkong9771/Spider/tree/main/Project%20Code/Picture/vmgirls_pictures) | [唯美图片下载](https://blog.csdn.net/qq_41447478/article/details/117418350) |
|         |                                                              |                                                              |





### 1.B站视频弹幕+词云分析

------

#### 0）项目自述

|   内容   |                             描述                             |
| :------: | :----------------------------------------------------------: |
| 项目时间 |                    2020.10.13-2020.10.16                     |
| 项目难度 |                         :star::star:                         |
| 完整代码 | [B站视频弹幕+词云分析](https://github.com/hongkong9771/Spider/tree/main/Project%20Code/Text/danmu/danmu_bilibili) |

#### 1）所需库的安装

```python
# 爬虫所需库
import requests		# 用于请求网页，获取html网页信息
import parsel		# 用于解析网页
import xlwt			# 用于excel表格制作
# 制作词云所需库
import xlrd			# 读取excel表格
from matplotlib import pyplot as plt	# 绘图
from PIL import Image		# 打开图像
from wordcloud import WordCloud	# 词云制作
import numpy as np		# 数组操作
import jieba.analyse	# jieba分词
```

#### 2）网页分析

​		本次爬取的B站视频网址为：[观察者网：【懂点儿啥】西方对外援助了这么多年，为何总失败？](https://www.bilibili.com/video/BV1aK4y1h7Hq?t=1021)

​		B站的弹幕信息位于页面最右边区域：

![1](https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/1.png)

​		按下F12键检查网页信息，可以发现弹幕每次只加载21条，而我们所需要的是获取到全部的弹幕信息。

![2](https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/2.png)

​		点击<font color=red>查看历史弹幕</font>，在右侧可以发现一个<font color=red>history</font>的文件，点击<font color=red>history</font>，再点击<font color=red>Preview</font>，可以查看弹幕内容。

![3](https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/3.png)

![4](https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/4.png)

​		该弹幕的URL则为：https://api.bilibili.com/x/v2/dm/history?type=1&oid=245944145&date=2020-10-22，想要爬取不同日期的弹幕，只需要修改后面的日期即可。

![5](https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/5.png)

#### 3）弹幕爬取

代码位于spider.py文件。

##### Ⅰ.获取网页信息

```python
def askurl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "cookie": "你的cookie信息"
    }
    response = requests.get(url=url, headers=head)
    html = response.content.decode("utf-8")
    """
    或者这样写也可以，两种写法都可以获得同样的网页信息
    response.encoding = 'utf-8'
    html = response.text
    """
    print(html)
    return html
```

得到如下信息：

![6](https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/6.png)

##### Ⅱ.爬取弹幕至列表

接着，获取弹幕信息：

```python
def getdata(baseurl):
    html = askurl(baseurl)
    parse = parsel.Selector(html)          # 解析html网页
    datalist = parse.xpath("//d/text()").getall()
    print(datalist)
    return datalist
```

- [<font color=red>`parsel`</font>](#1）parsel)：点击[<font color=red>`parsel`</font>](#1）parsel)跳转至附录介绍。
- [<font color=red>`xpath`</font>](#2）xpath)：点击[<font color=red>`xpath`</font>](#2）xpath)跳转至附录介绍。所有的弹幕信息都被保存至一个列表中。

所有的弹幕信息都被保存至一个列表中。

![7](https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/7.png)

##### Ⅲ.将弹幕保存至excel

```python
def savedata(datalist, savepath):
    print('saving...')
    danmu = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = danmu.add_sheet('B站弹幕', cell_overwrite_ok=True)  	# 创建工作表，工作表名为：B站弹幕
    col = ['序号', '弹幕']
    for i in range(0, 2):
        sheet.write(0, i, col[i])			  # 写入列名

    for i in range(len(datalist)):
        sheet.write(i + 1, 0, i+1)    		  # 序号写入
        sheet.write(i + 1, 1, datalist[i])    # 数据写入

    danmu.save(savepath)                      # 保存数据表
```

弹幕保存至excel结果图。

<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/8.png" alt="8" style="zoom:50%;" />

#### 4）词云制作

##### Ⅰ.进行jieba分词

将excel表格中的弹幕提取出来，并进行jieba分词，代码如下：

```python
import xlrd			# 读取excel表格
from matplotlib import pyplot as plt	# 绘图
from PIL import Image		# 打开图像
from wordcloud import WordCloud	# 词云制作
import numpy as np		# 数组操作
import jieba.analyse	# jieba分词


# 词云制作（分词）
data = xlrd.open_workbook("B站弹幕.xls", encoding_override='utf-8')  # 打开excel文件读取数据
table = data.sheets()[0]                    # 读取工作表，通过索引顺序获取
text = table.col_values(1)
# print(text) # text为一个列表
text_new = ""
for item in text[1:]:           # 去掉第一个值，即列名：弹幕
    text_new = text_new + item
    # print(item)
# print(text_new)
# print(len(text_new))

text_list = jieba.cut(text_new)                          # 进行jieba分词，将所有词全部切出来
# text_list = jieba.analyse.extract_tags(text_new, topK=50)  # 进行jieba分词，并且取频率出现最高的50个词
text_list = " ".join(text_list)          # jieba分词得到的text_list是列表形式的，需要将其以空格间隔开变为一个字符串形式
# print(type(text_list))
# print(len(text_list))
```

进行jieba分词后的效果。

![9](https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/9.png)

##### Ⅱ.词云制作

词云制作部分代码：

```python
# 词云制作（绘图）
img = Image.open(r'tree.jpg')
img_array = np.array(img)   # 将图片转换为数组
wc = WordCloud(
    width=1500,                 # 图片的宽度
    height=1000,                # 图片的高度
    background_color='white',   # 图片的背景色
    mask=img_array,
    contour_color="red",        # 图片边缘颜色
    contour_width=1,            # 图片边缘线条宽度
    font_path="msyh.ttc",       # 设置词云的字体，字体所在位置：C\Windows\Fonts
    # 设置屏蔽词
    stopwords={"哈哈哈", "哈哈哈哈", "哈哈"}
)
wc.generate_from_text(text_list)	# test_list为分好的词

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')     # 是否显示坐标轴
plt.show()  # 显示生成的词云图片
```

tree.jpg图片和词云图片。

<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/tree.jpg" alt="10" style="zoom:50%;" />
</div>



<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/B%E7%AB%99%E8%A7%86%E9%A2%91%E5%BC%B9%E5%B9%95+%E8%AF%8D%E4%BA%91%E5%88%86%E6%9E%90/10.png" alt="10" style="zoom:50%;" />
</div>





#### 5）完整代码

##### Ⅰ.弹幕爬取完整代码

```python
import requests		# 用于请求网页，获取html网页信息
import parsel		# 用于解析网页
import xlwt			# 用于excel表格制作


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
        "cookie": "your cookie"
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

```

##### Ⅱ.词云制作完整代码

```python
import xlrd			# 读取excel表格
from matplotlib import pyplot as plt	# 绘图
from PIL import Image		# 打开图像
from wordcloud import WordCloud	# 词云制作
import numpy as np		# 数组操作
import jieba.analyse	# jieba分词


# 词云制作（分词）
data = xlrd.open_workbook("B站弹幕.xls", encoding_override='utf-8')  # 打开excel文件读取数据
table = data.sheets()[0]                    # 读取工作表，通过索引顺序获取
text = table.col_values(1)
# print(text)
text_new = ""
for item in text[1:]:           # 去掉第一个值，即列名：弹幕
    text_new = text_new + item
    # print(item)
# print(text_new)
# print(len(text_new))


text_list = jieba.cut(text_new)                          # 进行jieba分词，将所有词全部切出来
# text_list = jieba.analyse.extract_tags(text_new, topK=10)  # 进行jieba分词，并且取频率出现最高的50个词
text_list = " ".join(text_list)                            # jieba分词得到的text_list是列表形式的，需要将其以空格间隔开变为一个字符串形式
print(text_list)
# print(len(text_list))

# 词云制作（绘图）
img = Image.open(r'tree.jpg')
img_array = np.array(img)   # 将图片转换为数组
wc = WordCloud(
    width=1500,                 # 图片的宽度
    height=1000,                # 图片的高度
    background_color='white',   # 图片的背景色
    mask=img_array,
    contour_color="red",        # 图片边缘颜色
    contour_width=1,            # 图片边缘线条宽度
    font_path="msyh.ttc",       # 设置词云的字体，字体所在位置：C\Windows\Fonts
    # 设置屏蔽词
    stopwords={"哈哈哈", "哈哈哈哈", "哈哈"}
)
wc.generate_from_text(text_list)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')     # 是否显示坐标轴
plt.show()  # 显示生成的词云图片
```



------

### 2.唯美图片下载

----

#### 0）项目自述

​		本项目的高级项目是在中级项目的基础上完成的，相较而言，代码更加工整，功能更加强大，因此，本次只介绍高级项目的完成过程。

##### 		Ⅰ.初级项目

​		下载不完全，且容易出现连接错误。

##### 		Ⅱ.中级项目

​		能够下载所有的专辑图片，但是未根据年份和月份分类下载并创建文件夹。

##### Ⅲ.高级项目

​		可以下载所有文件，并且可以根据年月份进行分类管理，自动创建相应的文件夹，若文件夹已存在，则跳过；在下载图片时，若图片已存在，则跳过，若不存在，则继续下载，相较于前面两个version，此版本有很大的提升。

​	在下载过程中如若出现下载错误，可能有以下几个原因：
​    1.网络状态不佳；
​    2.`headers`缺少`cookie`或者`Referer`信息；
​    3.短时间内多次访问该网址，被服务器远程断连，因此，在下载过程中需要加一个延时，避免过快过频繁的访问。

|       内容       |                             描述                             |
| :--------------: | :----------------------------------------------------------: |
| （初级）项目时间 |                    2020.10.16-2020.10.20                     |
| （初级）项目难度 |                         :star::star:                         |
| （中级）项目时间 |                    2020.11.11-2020.11.12                     |
| （中级）项目难度 |                      :star::star::star:                      |
| （高级）项目时间 |                    2020.11.19-2020.11.20                     |
| （高级）项目难度 |                   :star::star::star::star:                   |
|     完整代码     | [唯美图片下载](https://github.com/hongkong9771/Spider/tree/main/Project%20Code/Picture/vmgirls_pictures) |

#### 1）所需库的安装

```python
import requests					# 用于请求网页，获取html网页信息
import parsel					# 用于解析网页
from tqdm import tqdm, trange	# 用于添加进度条显示
import os						# 用于创建文件夹
import time						# 用于延迟下载
```

#### 2）网页分析

​		本次所要爬取的图片网页为：[vmgirls](https://www.vmgirls.com/archives.html).

​		进入网页我们可以看到所有的专辑图片都被按照日期分类整理好了，每一年包含不同的月份，每个月份又包含相应的日期，每个日期对应一个图片专辑，所以整个网页共有`83+152+362+672+28=`<font color=red>`1297`</font>个专辑。

<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/%E5%94%AF%E7%BE%8E%E5%9B%BE%E7%89%87%E4%B8%8B%E8%BD%BD/1.png" alt="1" style="zoom:30%;" />
</div>

##### Ⅰ.图片专辑网页分析

​		查看网页源代码如下图：

​		按<font color=red>年</font>分类：

<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/%E5%94%AF%E7%BE%8E%E5%9B%BE%E7%89%87%E4%B8%8B%E8%BD%BD/2.png" alt="2" style="zoom:60%;" />
</div>

​		按<font color=blue>月</font>分类：

<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/%E5%94%AF%E7%BE%8E%E5%9B%BE%E7%89%87%E4%B8%8B%E8%BD%BD/3.png" alt="3" style="zoom:50%;" />
</div>

​		按<font color=purple>专辑</font>分类:

<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/%E5%94%AF%E7%BE%8E%E5%9B%BE%E7%89%87%E4%B8%8B%E8%BD%BD/4.png" alt="4" style="zoom:50%;" />
</div>

​		观察可知，<font color=red>图片专辑链接</font>的网页代码十分规整，每一个专辑链接都有相同的标签路径和属性。

##### Ⅱ.图片网页分析

​		以日期为`2020.11.11`的第一个图片专辑为例：[温柔的秋日午后](https://www.vmgirls.com/15071.html)

<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/%E5%94%AF%E7%BE%8E%E5%9B%BE%E7%89%87%E4%B8%8B%E8%BD%BD/5.png" alt="5" style="zoom:70%;" />
</div>

​		所有的图片链接都被存放在属性名为<font color=red>`class`</font>，属性值为<font color=blue>`nc-light-gallery`</font>的<font color=purple>`div`</font>标签中，单个图片链接则保存在<font color=purple>`a`</font>标签中。因此可以按照以下方式提取单个图片的链接。

```python
links = parse.xpath('//div[@class="nc-light-gallery"]/a/img/@data-src').getall()
```

​		但是在实际提取链接的过程中，我们会发现，并不是所有的图片链接都是按照这样的规则排列的。因此，我们又根据实际情况添加了以下几个提取链接的方式，然后将多个链接提取整合在一起。

```python
links1 = parse.xpath('//div[@class="nc-light-gallery"]/a/img/@data-src').getall()    # 匹配大部分专辑图片
links2 = parse.xpath('//div[@class="nc-light-gallery"]/p/a/img/@data-src').getall()  # 有少部分专辑图片因为多加了一个p标签而无法匹配
links3 = parse.xpath('//div[@class="nc-light-gallery"]/figure/ul/li/figure/a/img/@data-src').getall()  # 同上
links4 = parse.xpath('//div[@class="nc-light-gallery"]/img/@data-src').getall()      # 有少部分专辑图片没有a标签
links = links1 + links2 + links3 + links4
```

​		在提取图片链接的过程中，可以根据遇到的各种问题来进行修改。

#### 3）图片专辑链接爬取

​		观察以上的网页代码，可以发现很容易提取到每个专辑的链接，这里我们利用`xpath`进行提取。

```python
import requests
import parsel
baseurl = "https://www.vmgirls.com/archives.html"
head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
response = requests.get(url=baseurl, headers=head)
html = response.text
parse = parsel.Selector(html)
names = parse.xpath('//ul[@class="al_mon_list"]/li/ul/li/a/text()').getall()
print(names)
```

​		输出每个专辑链接的名字:

<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/%E5%94%AF%E7%BE%8E%E5%9B%BE%E7%89%87%E4%B8%8B%E8%BD%BD/6.png" alt="6" style="zoom:60%;" />
</div>

```python
links = parse.xpath('//ul[@class="al_mon_list"]/li/ul/li/a/@href').getall()
print(links)
```

​		输出所有专辑链接：

<div align=center>
<img src="https://gitee.com/hongkong9771/csdn-blog-map-bed/raw/master/4.%E7%88%AC%E8%99%AB/%E5%94%AF%E7%BE%8E%E5%9B%BE%E7%89%87%E4%B8%8B%E8%BD%BD/7.png" alt="7" style="zoom:60%;" />
</div>

​		有了每个专辑的链接之后，接下来就是获取每个专辑的图片链接。

#### 4）图片下载

​		在图片下载过程中，将图片按照<font color=red>`年`</font>、<font color=blue>`月`</font>和<font color=purple>`专辑`</font>进行分类下载，便于分类管理。

##### Ⅰ.提取<font color=red>`年`</font>和<font color=blue>`月`</font>的名称

​		将<font color=red>`年`</font>和<font color=blue>`月`</font>的名称提取出来，用作文件夹命名。

```python
import requests
import parsel
baseurl = "https://www.vmgirls.com/archives.html"
head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0;"
                      "_gads=ID=5cf3e347dd6b2d84-229b22aa1bc400f7:T=1602834524:RT=1602834524:S=ALNI_ManB5ea_g7S5PZe0TKNxBzkX5j1uA; Hm_lvt_a5eba7a40c339f057e1c5b5ac4ab4cc9=1602832999,1603073523,1605085840,1605235089; _GPSLSC=; Hm_lpvt_a5eba7a40c339f057e1c5b5ac4ab4cc9=1605235201"
    }
response = requests.get(baseurl, headers=head)
html = response.text
parse = parsel.Selector(html)
name_year = parse.xpath('//h4/text()').getall()
name_month = parse.xpath('//span[@class="al_mon"]//text()').getall()
print(name_year)
print(name_month)
```

​		提取结果如下：

```python
['2020 年【85】', '2019 年【152】', '2018 年【362】', '2017 年【672】', '2016 年【28】']
['11 月 [9]', '10 月 [14]', '09 月 [23]', '07 月 [16]', '06 月 [2]', '05 月 [4]', '04 月 [10]', '02 月 [4]', '01 月 [3]', '12 月 [12]', '11 月 [3]', '10 月 [12]', '09 月 [14]', '08 月 [10]', '07 月 [3]', '06 月 [13]', '05 月 [24]', '04 月 [10]', '03 月 [9]', '02 月 [19]', '01 月 [23]', '12 月 [15]', '11 月 [29]', '10 月 [9]', '09 月 [17]', '08 月 [23]', '07 月 [34]', '06 月 [24]', '05 月 [13]', '04 月 [27]', '03 月 [65]', '02 月 [40]', '01 月 [66]', '12 月 [51]', '11 月 [66]', '10 月 [41]', '09 月 [15]', '08 月 [33]', '07 月 [32]', '06 月 [25]', '05 月 [49]', '04 月 [74]', '03 月 [83]', '02 月 [143]', '01 月 [60]', '12 月 [16]', '11 月 [5]', '10 月 [4]', '06 月 [2]', '05 月 [1]']
```

##### Ⅱ.提取<font color=red>`年`</font>和<font color=blue>`月`</font>中的数字

​		将<font color=red>`年`</font>的和<font color=blue>`月`</font>中的专辑数量提取出来，用于设置文件夹分类时的停止条件。

```python
# 每年的专辑数量
number_year = []
for i in range(len(name_year)):
	number_year_former = name_year[i].index(name_year[i][6])
    number_year_latter = name_year[i].index(name_year[i][-1])
   	year = name_year[i][number_year_former + 1:number_year_latter]
    number_year.append(year)
    # number_year = int(number_year)
	print(number_year)

#  每个月的专辑数量
number_month = []
for i in range(len(name_month)):
	number_month_former = name_month[i].index(name_month[i][5])
	number_month_latter = name_month[i].index(name_month[i][-1])
	month = name_month[i][number_month_former + 1:number_month_latter]
	number_month.append(month)
    print(number_month)
```

​		提取结果如下：

```python
['85', '152', '362', '672', '28']
['9', '14', '23', '16', '2', '4', '10', '4', '3', '12', '3', '12', '14', '10', '3', '13', '24', '10', '9', '19', '23', '15', '29', '9', '17', '23', '34', '24', '13', '27', '65', '40', '66', '51', '66', '41', '15', '33', '32', '25', '49', '74', '83', '143', '60', '16', '5', '4', '2', '1']
```

##### Ⅲ.制定文件夹分类

```python
urls = list(range(0,1299))
# print(len(urls))
month_index = 0
urls_index = 0
j = 0
for i in range(len(number_year)):
    print(name_year[i])    # 每个年份的名字（用作文件夹名）
    sum_month = 0
    month_index += j       # 每年的月份个数（累加）
    print(month_index)
    for j in range(len(number_month[month_index:])):
        each_month = int(number_month[j+month_index])      # 每个月的专辑数
        sum_month += each_month
        print(name_month[j+month_index],end=' ')           # 每个月份的名字（用作文件夹名）
        print(urls[urls_index:(urls_index + each_month)])  # 每个月的专辑链接
        urls_index += each_month
        if sum_month == int(number_year[i]):
            j += 1
            print('\n')
            break
```

​		文件夹分类结果如下：

​		年份文件夹<font color=red>`2020 年【85】`</font>为第一级目录，月份文件夹<font color=blue>`11 月`</font>为第二级目录，专辑名（对应下面的专辑序号）为第三级目录，图片保存在相应的专辑文件夹中。

```python
2020 年【85】
0
11 月 [9] [0, 1, 2, 3, 4, 5, 6, 7, 8]
10 月 [14] [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
09 月 [23] [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
07 月 [16] [46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]
06 月 [2] [62, 63]
05 月 [4] [64, 65, 66, 67]
04 月 [10] [68, 69, 70, 71, 72, 73, 74, 75, 76, 77]
02 月 [4] [78, 79, 80, 81]
01 月 [3] [82, 83, 84]

2019 年【152】
9
12 月 [12] [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96]
11 月 [3] [97, 98, 99]
10 月 [12] [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]
09 月 [14] [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]
08 月 [10] [126, 127, 128, 129, 130, 131, 132, 133, 134, 135]
07 月 [3] [136, 137, 138]
06 月 [13] [139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151]
05 月 [24] [152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175]
04 月 [10] [176, 177, 178, 179, 180, 181, 182, 183, 184, 185]
03 月 [9] [186, 187, 188, 189, 190, 191, 192, 193, 194]
02 月 [19] [195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213]
01 月 [23] [214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236]

2018 年【362】
21
12 月 [15] [237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251]
11 月 [29] [252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280]
10 月 [9] [281, 282, 283, 284, 285, 286, 287, 288, 289]
09 月 [17] [290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306]
08 月 [23] [307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329]
07 月 [34] [330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363]
06 月 [24] [364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387]
05 月 [13] [388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400]
04 月 [27] [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427]
03 月 [65] [428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492]
02 月 [40] [493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532]
01 月 [66] [533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598]

2017 年【672】
33
12 月 [51] [599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649]
11 月 [66] [650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715]
10 月 [41] [716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756]
09 月 [15] [757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771]
08 月 [33] [772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804]
07 月 [32] [805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836]
06 月 [25] [837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861]
05 月 [49] [862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910]
04 月 [74] [911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984]
03 月 [83] [985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067]
02 月 [143] [1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210]
01 月 [60] [1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1259, 1260, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 1268, 1269, 1270]

2016 年【28】
45
12 月 [16] [1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286]
11 月 [5] [1287, 1288, 1289, 1290, 1291]
10 月 [4] [1292, 1293, 1294, 1295]
06 月 [2] [1296, 1297]
05 月 [1] [1298]
```

##### Ⅳ.文件判定

​		在创建一个文件夹时，需要先判断文件夹是否已经存在。若存在，则跳过创建过程；若不存在，则创建该文件夹。同理可知，在下载图片时，也需要判断图片是否已经下载，若已下载，则跳过下载过程；若未下载，则下载该图片。

```python
# 为每个专辑创建一个文件夹，每个专辑存放在对应的年份和月份文件夹中
# 文件夹创建时只能一级一级的创建，不能一下子创建多级文件夹
def createdir(name_year, name_month, dir_name):
    if not os.path.exists(name_year):
        os.mkdir(name_year)
    if not os.path.exists(name_year + '/' + name_month):
        os.mkdir(name_year + '/' + name_month)
    if not os.path.exists(name_year + '/' + name_month + '/' + dir_name):
        os.mkdir(name_year + '/' + name_month + '/' + dir_name)
        
def download(name_year, name_month, dir_name, urls, head):
    for url in urls:
        file_name = urls.index(url) + 1
        if not os.path.exists(name_year + '/' + name_month + '/' + dir_name + '/' + str(file_name) + ".jpg"):
            if "https:" not in url:
                url = "https:" + url
            response = requests.get(url, headers=head)
            with open(name_year + '/' + name_month + '/' + dir_name + '/' + str(file_name) + ".jpg", 'wb') as f:
                f.write(response.content)
                time.sleep(15)
```

#### 5）完整代码

```python
import requests
import parsel
from tqdm import tqdm, trange
import os
import time


def main():
    baseurl = "https://www.vmgirls.com/archives.html"
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "cookie": "your cookie"
    }
    name_year, name_month, number_year, number_month = file_path_name(baseurl, head)
    html = askurl(baseurl, head)
    names, urls = getlinks(html)        # 所有专辑的名字和链接
    # print(len(urls))
    '''
    可以设置从断点处下载，更改下面month_index和urls_index的值。
    当专辑下载断连时，需要考虑sum_month的值，，在跳转年份文件夹时，需要重新初始化为0；
    month_index：月份链接索引
    urls_index：专辑链接索引
    二者必须匹配
    '''
    month_index = 0     # 月份链接索引
    urls_index = 0     # 专辑链接索引
    j = 0
    for i in range(len(number_year)):
        # print(name_year[i])     # 每个年份的名字（用作文件夹名）
        sum_month = 0
        month_index += j        # 每年的月份个数（累加）
        # print(month_index)
        # if i == 0 or i == 1 or i == 2:      # 跳过2020、2019、2018年的下载（根据下载需要进行设置 ）
            # continue
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
            urls_index += each_month
            if sum_month == int(number_year[i]):
                j += 1
                # print('\n')
                break
            time.sleep(60)


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
    links = links1 + links2 + links3 + links4
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
                time.sleep(15)
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

```

