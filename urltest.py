from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re

def getTitle(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html,"html.parser")
        title = bsObj.title
    except AttributeError as e:
        return None
    return title

def getImg(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html,"html.parser")
        images = bsObj.findAll("img")
    except AttributeError as e:
        return None
    return images

url = "https://www.zhihu.com/question/34243513/"
title = getTitle(url)
image = getImg(url)
imgNum = len(image)
if title == None:
    print("No Title To Show!")
else:
    print("在网页："+title.get_text())
if imgNum == 0 :
    print("页面上没有图片\n")
else:
    print("共找到%d张图片"%len(image))
    for img in image:
        print(img["src"])


