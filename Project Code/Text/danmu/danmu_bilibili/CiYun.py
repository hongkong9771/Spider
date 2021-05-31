# -*- coding : utf-8 -*- 
# @Time : 2020/10/14 15:15
# @Author : 危红康
# @File : CiYun.py
# @Software: PyCharm


import xlrd
from matplotlib import pyplot as plt
from PIL import Image
from wordcloud import WordCloud
import numpy as np
import jieba.analyse


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

'''
# 检测输出是否正确
out = open('out.txt', 'w', encoding='utf-8')
out.write(text_new)
out.close()
'''

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
