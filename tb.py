#coding:gbk
import urllib
import urllib2
import re

#����ҳ���ǩ��
class Tool:
    #ȥ��img��ǩ,7λ���ո�
    removeImg = re.compile('<img.*?>| {7}|')
    #ɾ�������ӱ�ǩ
    removeAddr = re.compile('<a.*?>|</a>')
    #�ѻ��еı�ǩ��Ϊ\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #�������Ʊ�<td>�滻Ϊ\t
    replaceTD= re.compile('<td>')
    #�Ѷ��俪ͷ��Ϊ\n�ӿ�����
    replacePara = re.compile('<p.*?>')
    #�����з���˫���з��滻Ϊ\n
    replaceBR = re.compile('<br><br>|<br>')
    #�������ǩ�޳�
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()��ǰ���������ɾ��
        return x.strip()
 
 
#�ٶ�����������
class BDTB:
 
    #��ʼ�����������ַ���Ƿ�ֻ��¥���Ĳ���
    def __init__(self,baseUrl,seeLZ,floorTag):
        #base���ӵ�ַ
        self.baseURL = baseUrl
        #�Ƿ�ֻ��¥��
        self.seeLZ = '?see_lz='+str(seeLZ)
        #HTML��ǩ�޳����������
        self.tool = Tool()
        #ȫ��file�������ļ�д���������
        self.file = None
        #¥���ţ���ʼΪ1
        self.floor = 1
        #Ĭ�ϵı��⣬���û�гɹ���ȡ������Ļ�������������
        self.defaultTitle = "�ٶ�����"
        #�Ƿ�д��¥�ָ����ı��
        self.floorTag = floorTag
 
    #����ҳ�룬��ȡ��ҳ���ӵĴ���
    def getPage(self,pageNum):
        try:
            #����URL
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #����UTF-8��ʽ��������
            return response.read().decode('utf-8')
        #�޷����ӣ�����
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print "���Ӱٶ�����ʧ��,����ԭ��",e.reason
                return None
 
    #��ȡ���ӱ���
    def getTitle(self,page):
        #�õ�������������ʽ
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        result = re.search(pattern,page)
        if result:
            #������ڣ��򷵻ر���
            return result.group(1).strip()
        else:
            return None
 
    #��ȡ����һ���ж���ҳ
    def getPageNum(self,page):
        #��ȡ����ҳ�����������ʽ
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    #��ȡÿһ��¥������,����ҳ������
    def getContent(self,page):
        #ƥ������¥�������
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            #���ı�����ȥ����ǩ������ͬʱ��ǰ����뻻�з�
            content = "\n"+self.tool.replace(item)+"\n"
            contents.append(content.encode('utf-8'))
        return contents

    # def getUserid(self,page):
    #     #ƥ��ÿ��¥��Ĳ���ID
    #     pattern = re.compile('<a data-field="{.*?>(.*?)</a>',re.S)
    #     items = re.findall(pattern,page)
    #     print "test:"
    #     for i in items:
    #         print i+"..."
    #     contents = []
    #     for item in items:
    #         content = "\n"+self.tool.replace(item)+"\n"
    #         contents.append(content.encode('utf-8'))
    #     return contents

    def setFileTitle(self,title):
        #������ⲻ��ΪNone�����ɹ���ȡ������
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")

    def writeData(self,contents):
        #���ļ�д��ÿһ¥����Ϣ
        for item in contents:
            if self.floorTag == '1':
                #¥֮��ķָ���
                floorLine = "\n" + str(self.floor) + "L----------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL��ʧЧ��������"
            return
        try:
            print "�����ӹ���" + str(pageNum) + "ҳ"
            for i in range(1,int(pageNum)+1):
                print "����д���" + str(i) + "ҳ����"
                page = self.getPage(i)
                #self.getUserid(page)
                contents = self.getContent(page)
                #self.writeData(ids)
                self.writeData(contents)
        #����д���쳣
        except IOError,e:
            print "д���쳣��ԭ��" + e.message
        finally:
            print "д���������"
 
 
 
print "���������Ӵ���"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input('http://tieba.baidu.com/p/'))
seeLZ = raw_input("�Ƿ�ֻ��ȡ¥�����ԣ�������1��������0\n")
floorTag = raw_input("�Ƿ�д��¥����Ϣ��������1��������0\n")
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()