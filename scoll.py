from urllib.request import urlopen
from selenium import webdriver
import re
import os
import time

def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        print ('新建了名字叫做',path,'的文件夹')
        os.makedirs(path)
        return True
    else:
        print ('名为',path,'的文件夹已经创建成功')
        return False

print("Loading... ")
driver = webdriver.PhantomJS(executable_path="C://python//phantomjs//bin//phantomjs")
driver.get("https://www.zhihu.com/question/37787176")
title = driver.title
print(title)
mkdir("D://py_imgs//"+title)
# time.sleep(5)
print("正在读取页面图片...")
driver.execute_script("""
        (function () {
            var y = document.body.scrollTop;
            var step = 500;
            window.scroll(0, y);
            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 50);
                }
                else {
                    window.scroll(0, y);
                    document.title += "scroll-done";
                }
            }
            setTimeout(f, 100);
        })();
        """)

time.sleep(35)

img = driver.find_elements_by_tag_name('img')
i = 1
for image in img:
    src = image.get_attribute('src')
    u = urlopen(src)
    data = u.read()
    if len(data) >= 5120 :
        f = open("D://py_imgs//"+title + "//" + str(i) + ".jpg","wb+")
        f.write(data)
        print('正在写入第 %d 张图片...'%i)
        i = i + 1
print("Completed !")
driver.close
