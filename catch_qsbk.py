#!/usr/bin/python
# coding=utf-8


"""
1.抓取糗事百科热门段子
2.过滤带有图片的段子
3.实现每按一次回车显示一个段子的发布时间，发布人，段子内容，点赞数
"""

import re
import urllib
import urllib2


# 糗事百科爬虫类
class QSBK:
    # 初始化函数
    def __init__(self):
        self.pageindex = 1
        # 设置用户身份，模拟IT浏览器包头
        self.usr_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化包头，设置为一个字典
        self.headers = {'User-Agent': self.usr_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 程序是否连续运行标志
        self.enable = False

    def getpage(self, pageindex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageindex)
            # 构建请求repuest对象
            request = urllib2.Request(url, headers=self.headers)
            # 通过request对象获取页面代码对象
            respones = urllib2.urlopen(request)
            # 读取页面内容
            content = respones.read().decode('utf-8')
            return content

        except urllib2.URLError, e:
            # hasattr判断object中是否有name属性，返回一个布尔值
            if hasattr(e, 'reason'):
                print u"连接糗事百科失败,错误原因", e.reason
                return None

    def get_content(self, index):
        page_content = self.getpage(index)
        if not page_content:
            print 'page load wrong!'
            return None
        # 1）.*? 是一个固定的搭配，.和*代表可以匹配任意无限多个字符，加上？表示使用非贪婪模式进行匹配，也就是我们会尽可能

        # 短地做匹配，以后我们还会大量用到 .*? 的搭配。

        # 2）(.*?)代表一个分组，在这个正则表达式中我们匹配了五个分组，在后面的遍历item中，item[0]就代表第一个(.*?)
        # #所指代的内容，item[1]就代表第二个(.*?)所指代的内容，以此类推。

        # 3）re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。

        # 设置正则表达式寻找要的字符
        pattern = re.compile(
            "<h2>(.*?)</h2>.*?content\">(.*?)</div>(.*?)\"number\">(.*?)</i.*?number\">(.*?)</", re.S)
        items = re.findall(pattern, page_content)
        pagestories = []
        # item中代表的是 上传者 内容 可能包含图片的代码  点赞数 评论数
        for item in items:
            # 查找是否包含图片
            haveimg = re.search("img", item[2])
            if not haveimg:
                # 将回车换成\n
                replace = re.compile("<br/>")
                text = re.sub(replace, "\n", item[1])
                # 去掉两边的可能空格,作为列表插入
                pagestories.append([item[0].strip(), text.strip(), item[3].strip(), item[4].strip()])
        return pagestories

    def loadPage(self):
        if self.enable:
            if len(self.stories) < 2:
                page = self.get_content(self.pageindex)
                if page:
                    self.stories.append(page)
                    self.pageindex += 1

    def getonestory(self, pagestorys, page):
        input = raw_input()
        if input.lower() == "q":
            self.enable = False
            return
        self.loadPage()
        for story in pagestorys:
            print u"第%d页\t发布人:%s\t赞:%s\t评论:%s\n%s\n" % (page, story[0], story[2], story[3], story[1])

    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pagestory = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getonestory(pagestory, nowPage)

if __name__=="__main__":
    spider = QSBK()
    spider.start()