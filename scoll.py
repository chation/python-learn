from urllib.request import urlopen
from selenium import webdriver
import os
import time

# 配置选项
FONT_PATH = "D://py_imgs//"
PAGE_PATH = "https://www.zhihu.com/question/22918070"

def formatStr(title):
    'windows系统文件夹不能包含如下字符'
    title = title.replace('/','')
    title = title.replace('\\','')
    title = title.replace('?','')
    title = title.replace('|','')
    title = title.replace('*','')
    title = title.replace('.','')
    title = title.replace('\"','')
    title = title.replace(':','')
    title = title.replace('>','')
    title = title.replace('<','')

    return title

def mkdir(path):
    '创建文件夹'
    path = path.strip()
    isExists = os.path.exists(FONT_PATH+path)
    if not isExists:
        print ('新建了名字叫做',path,'的文件夹')
        os.makedirs(FONT_PATH+path)
        return True
    else:
        print ('名为',path,'的文件夹已经创建成功')
        return False

print("Loading... ")
driver = webdriver.PhantomJS(executable_path="C://python//phantomjs//bin//phantomjs")
driver.get(PAGE_PATH)
title = driver.title
print(title)

title = formatStr(title)
mkdir(title)
print("正在读取页面图片...")

# 页面下拉载入图片
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
# 等待载入
time.sleep(35)

# 获取页面所有图片
img = driver.find_elements_by_tag_name('img')
i = 0
for image in img:
    src = image.get_attribute('src')
    u = urlopen(src)
    data = u.read()
    # 判断是否有效图片
    if len(data) >= 5120 :
        f = open(FONT_PATH + title + "//" + str(i+1) + ".jpg","wb+")
        f.write(data)
        print('正在写入第 %d 张图片...'%(i+1))
        i = i + 1
if i == 0 :
    print("no picture found!")

print("Completed !")
driver.close()