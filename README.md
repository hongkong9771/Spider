## Spider

始于2020.10.10

闲暇之际，爬虫自娱。



本系列按照所爬取内容的格式，共分为以下几种：

| 内容    | 项目名称（代码链接）                                         | CSDN详解链接                                                 |
| ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Text    | [B站视频弹幕+词云分析](https://github.com/hongkong9771/Spider/tree/main/Project%20Code/Text/danmu/danmu_bilibili) | [B站视频弹幕+词云分析](https://blog.csdn.net/qq_41447478/article/details/117416669) |
| Picture |                                                              |                                                              |
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



### A.附录

---

#### 1.常见库的使用

##### 1）parsel

还未更新完全......

##### 2）xpath

​		<font color=red>`xpath`</font>全称为<font color=blue>`XML Path Language`</font>，是一种小型的查询语言，在网页分析上比<font color=red>`re`</font>更具有优势，其可以在XML和HTML中查找有用信息，可以通过元素和属性进行导航。<font color=red>`xpath`</font>的基本语法在[菜鸟教程](https://www.runoob.com/xpath/xpath-tutorial.html)里有详细的讲解，这里就不过多赘述了，主要罗列一些笔者在爬虫过程中常用的方法。

| 表达式      | 作用                                                         |
| :---------- | :----------------------------------------------------------- |
| //          | 定位根节点，会对全文进行扫描，在文档中选取所有符合条件的内容，以列表的形式返回。 |
| /           | 寻找当前标签路径的下一层路径标签或者对当前路标签内容进行操作。 |
| /**text()** | 获取当前路径下的文本内容。                                   |
| **/@xxxx**  | 获取属性名为**xxxx**的属性值。                               |
| \|          | 可选符，使用\|可选取若干个路径 如//p\|//div 即在当前路径下选取所有符合条件的p标签和div标签。 |
| .           | 选取当前节点。                                               |
| ..          | 选取当前节点的父节点。                                       |

```html
# html网页html="""    <!DOCTYPE html>    <html>        <head lang="en">        <title>测试</title>        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />        </head>        <body>            <div id="content">                <ul id="ul">                    <li>NO.1</li>                    <li>NO.2</li>                    <li>NO.3</li>                </ul>                <ul id="ul2">                    <li>one</li>                    <li>two</li>                </ul>            </div>            <div id="url">                <a href="http:www.58.com" title="58">58</a>                <a href="http:www.csdn.net" title="CSDN">CSDN</a>            </div>        </body>    </html>"""
```

- 代码示例1

```python
import parselparse = parsel.Selector(html)content = parse.xpath('//div[@id="content"]/ul[@id="ul"]/li/text()').getall()	# 这里使用id属性来定位哪个div和ul被匹配 使用text()获取文本内容for i in content:    print(i)
```

```python
NO.1NO.2NO.3
```

- 代码示例2

```python
content = parse.xpath('//a/@href').getall() #这里使用//从全文中定位符合条件的a标签，使用“@标签属性”获取a标签的href属性值for each in content:    print(each)
```

```python
http:www.58.comhttp:www.csdn.net
```

- 代码示例3

```python
# content = parse.xpath('/html/body/div/a/@title').getall() # 使用绝对路径定位a标签的title# content = parse.xpath('//a/@title').getall() # 使用相对路径定位a标签的titlecontent = parse.xpath('//a/text()').getall() #首先定位到a标签，然后使用text()获取文本内容，虽然与上面两种方法获取到的值一样，但是获取内容的地方是不一样的。for i in content:    print (i)
```

```python
58CSDN
```

​		[CSDN](https://blog.csdn.net/Winterto1990/article/details/47903653)中关于<font color=red>`xpath`</font>的一个讲解，还可以。本节示例就是参考的这个博客。[知乎专栏](https://zhuanlan.zhihu.com/p/29436838)也有一个不错的介绍。

----

#### 2.项目难度指标

----

##### 1）1颗星:star:

##### 2）2颗星:star::star:

##### 3）3颗星:star::star::star:

##### 4）4颗星:star::star::star::star:

##### 5）5颗星:star::star::star::star::star:

##### 6）6颗星:star::star::star::star::star::star:
