#coding=utf-8
from urllib.request import urlopen
html = urlopen("http://192.168.1.109")
print(html.read())
