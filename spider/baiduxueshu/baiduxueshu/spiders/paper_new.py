# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
from urllib import parse
from spider.baiduxueshu.baiduxueshu.items import *
from spider.baiduxueshu.baiduxueshu.spiders import mysql
from spider.baiduxueshu.baiduxueshu import settings


class PaperSpider(scrapy.Spider):
    name = 'paper_new'
    allowed_domains = []
    start_urls = ['http://www.baidu.com/']
    db_chen = mysql.DB('chen')


    def parse(self, response):
        yield scrapy.Request('http://www.hao123.com/', callback=self.Myparse, dont_filter=True)

        # url = 'http://xueshu.baidu.com/usercenter/paper/show?paperid=81af121ddd2189c692dddb0419e135b4&site=xueshu_se'
        # yield scrapy.Request(url, callback=self.PaperInfo, dont_filter=True)

    # 查询 导师姓名和学习，并 加入爬取队列
    def Myparse(self, response):
        sql = 'SELECT * FROM `eds_paper_search_list` WHERE search=0'
        for teacher in self.db_chen.getDics(sql):
            # teacher = self.db_chen.getDics(sql)[0]
            # sql = 'UPDATE eds_paper_search_list SET searching=1 WHERE id=%s'
            # self.db_chen.exe_sql(sql,teacher['id'] )
            url = "http://xueshu.baidu.com/s?wd=%22" + teacher['name'] + "%22+%22" + teacher[
                'school'] + "%22+author%3A%28" + teacher[
                      'name'] + "%29&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=1&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=2"
            request = scrapy.Request(url, callback=self.PaperList ,dont_filter=True)
            request.meta['teacher'] = teacher
            yield request


    # 百度学术list页面，对于每个项，保存一部分信息，然后请求具体信息
    def PaperList(self, response):
        teacher = response.meta['teacher']

        # print('*'*10,response.url)
        list = response.xpath("//div[@class='result sc_default_result xpath-log']")
        for node in list:
            item = PaperItem()
            item['author_id'] = teacher['id']
            # 文章名字 + url
            name_t1 = node.xpath("./div[1]/h3/a")
            item['name'] = self.setValue(name_t1.xpath('string(.)'), "", 0)
            url_t1 = self.setValue(node.xpath("./div[1]/h3/a/@href"), "", 0)
            pid = re.findall('%3A%28(.+?)%29',url_t1)[0]
            item['paper_md5'] = pid
            item['url'] = 'http://xueshu.baidu.com/usercenter/paper/show?paperid=%s&site=xueshu_se'%pid
            # 文章发表期刊
            item['org'] = self.setPaperOrg(node)
            # 文章年份
            year_t1= self.setValue(node.xpath("./div[1]/div[2]/span[4]/text()"), "", 0)
            item['year'] = ''.join(re.findall('[0-9]+',year_t1))
            # 文章被引数
            item['cited_num'] = self.setPaperCite(node)

            request = scrapy.Request(item['url'], callback=self.PaperInfo,headers={"Referer": None},dont_filter=True)
            request.meta['item'] = item
            yield request
        a = response.xpath("//p[@id='page']/a")
        sflag = 0
        for node in a:
            b = self.setValue(node.xpath("./i"), "", 0)
            if b.find('pager-next')!=-1:
                sflag = 1
                url = "http://xueshu.baidu.com" + self.setValue(node.xpath("./@href"), "", 0)
                fpage = self.setValue(response.xpath("//span[@class='pc']/text()"), "", 0)
                if int(fpage) < settings.MAX_PAGE:
                    request = scrapy.Request(url, callback=self.PaperList , headers={"Referer": None} , dont_filter=True)
                    request.meta['teacher'] = teacher
                    yield request
                else:
                    sflag = 0
        if sflag == 0:
            sql = 'UPDATE eds_paper_search_list SET search=1 WHERE id=%s'
            self.db_chen.exe_sql(sql, teacher['id'])


    #每篇文章的具体信息页面，保存部分信息，请求源url以获取摘要
    def PaperInfo(self,response):


        item = response.meta['item']

        paper_author_list = response.xpath("//div[@class='author_wr']/p[2]/span")
        item['author'] = self.getAuthorOrg(paper_author_list)

        keyword_list = response.xpath("//div[@class='kw_wr']/p[2]/span")
        kw = []
        for node in keyword_list:
            kw.append(self.setValue(node.xpath("./a/text()"), "", 0))
        item['keyword'] = ','.join(kw)

        paper_sourceURL = self.setValue(response.xpath("//div[@class='subinfo_tool']/a[1]/@data-url"), "", 0)
        #---源地址集合---
        source_dic = {}
        source_list = response.xpath("//div[@class='allversion_content']/span")
        for node in source_list:
            source = self.setValue(node.xpath("./a/span[2]/text()"), "", 0)
            source_url = self.setValue(node.xpath("./a/@data-url"), "", 0)
            source_dic[source] = source_url

        #构造 引用、参考链接
        item['cited_url'] = ''
        item['reference_url'] = ''

        if source_dic.setdefault(settings.ABSTRACT_PRIORITY['1'],None):
            item['source'] = settings.ABSTRACT_PRIORITY['1']
            item['source_url'] = source_dic[settings.ABSTRACT_PRIORITY['1']]
        elif source_dic.setdefault(settings.ABSTRACT_PRIORITY['2'],None):
            item['source'] = settings.ABSTRACT_PRIORITY['2']
            item['source_url'] = source_dic[settings.ABSTRACT_PRIORITY['2']]
        elif source_dic.setdefault(settings.ABSTRACT_PRIORITY['3'], None):
            item['source'] = settings.ABSTRACT_PRIORITY['3']
            item['source_url'] = source_dic[settings.ABSTRACT_PRIORITY['3']]
        else:
            item['source'] = ''
            item['source_url'] = paper_sourceURL

        abstract = self.setValue(response.xpath("//p[@class='abstract']/text()"), "", 0)

        #---如果百度学术页面摘要不全，再去源链接找摘要---
        if abstract[-3:]=="...":
            if item['source'] == '知网':
                request = scrapy.Request(item['source_url'], callback=self.CNKI_Abstract)
                request.meta['item'] = item
                yield request
            elif item['source'] == '万方':
                # time.sleep(20)
                request = scrapy.Request(item['source_url'], callback=self.WANFANG_Abstract)
                request.meta['item'] = item
                yield request
            elif item['source'] == '维普':
                # time.sleep(20)
                request = scrapy.Request(item['source_url'], callback=self.VIP_Abstract,headers=settings.VIP_HEADERS)
                request.meta['item'] = item
                yield request
        else:
            item['abstract'] = abstract
            yield item

    #---知网解析---
    def CNKI_Abstract(self, response):
        item = response.meta['item']
        if len(re.findall('http://kns', response.url)) > 0:
            item['abstract'] = self.setValue(response.xpath("//span[@id='ChDivSummary']/text()"), "", 0)
            if item['author'] == "":  # 如果之前作者为空，则在源链接里面再存一遍作者和单位
                author_list = response.xpath("//div[@class='author']/span/a/text()").extract()
                item['author'] = self.getAbstractAuthor(author_list)
        else:
            # 存储摘要
            item['abstract'] = self.setValue(response.xpath("//div[@class='xx_font'][1]/text()"), "", 1)
            if item['author'] == "":  # 如果之前作者为空，则在源链接里面再存一遍作者和单位
                author_list = response.xpath("//div[@id='content']/div[2]/div[3]/a/text()").extract()
                item['author'] = self.getAbstractAuthor(author_list)
        yield item

    # ---万方解析---
    def WANFANG_Abstract(self, response):
        item = response.meta['item']
        # 有两种类型的链接，分类处理
        if len(re.findall('http://d.g', response.url)) > 0:
            item['abstract'] = self.setValue(response.xpath("//div[@class='abstract']/textarea/text()"), "", 0)
            if item['author'] == "":  # 如果之前作者为空，则在源链接里面再存一遍作者和单位
                author_list = response.xpath(
                    "//table[@id='perildical_dl']/tr[1]/td/a/text() | //table[@id='perildical2_dl']/tr[1]/td/a/text()").extract()
                item['author'] = self.getAbstractAuthor(author_list)
        else:
            item['abstract'] = self.setValue(response.xpath("//div[@class='abstract']/textarea/text()"), "", 0)
            if item['author'] == "":  # 如果之前作者为空，则在源链接里面再存一遍作者和单位
                author_list = response.xpath("//div[@class='row row-author']/span[2]/a/text()").extract()
                item['author'] = self.getAbstractAuthor(author_list)
        yield item

    # ---维普解析---
    def VIP_Abstract(self, response):
        item = response.meta['item']
        # 存储摘要
        item['abstract'] = self.setValue(response.xpath("//td[@class='sum']/text()"), "", 2)
        if item['author'] == "":  # 如果之前作者为空，则在源链接里面再存一遍作者和单位
            list = response.xpath("//span[@class='detailtitle']/strong/i/a/text()").extract()
            author_list = []
            for i in range(0, len(list)):
                if len(list[i]) in range(1, 4):
                    author_list.append(list[i])
            item['author'] = self.getAbstractAuthor(author_list)
        yield item

    #---------------------------------------------------
    #-                下面是功能函数                      -
    #---------------------------------------------------
    # 解析 作者和机构，如果没有就返回空
    def getAuthorOrg(self, paper_author_list):
        name_list = paper_author_list.xpath("./a/text()").extract()
        url_list = paper_author_list.xpath("./a/@href").extract()
        if (len(name_list) == len(url_list) and len(name_list) < 6):
            paper_author_out = "["
            for i in range(0, len(url_list)):
                t = re.findall(r'[\u4E00-\u9FA5]+', parse.unquote(url_list[i]))
                print(t)
                if len(t) >= 2:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (name_list[i], t[1])
                elif len(t) == 1:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (name_list[i], "")
                elif len(t) == 0:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (
                        name_list[i].replace("\r\n        ", ""), "")
                else:
                    return ""
            return paper_author_out.rstrip(',') + ']'
        else:
            return ""

    # 判断xpath取值是否为空，若为空则返回空字符（避免异常）
    def setValue(self, node, value, index):
        if len(node):
            return node.extract()[index].strip()
        else:
            return value

    # 取文章发表的期刊机构
    def setPaperOrg(self, node):
        data = node.xpath("./div[1]/div[2]/span[2]/a")
        if len(data):
            return self.setValue(data.xpath('string(.)'),'',0)
        else:
            tnode = node.xpath("./div[1]/div[2]/span[2]")
            return self.setValue(tnode.xpath('string(.)'), '', 0)

    # 取文章发表的引用量
    def setPaperCite(self, node):
        data = node.xpath("./div[1]/div[2]/span[3]/a")
        if len(data):
            return int(data.xpath('string(.)').extract()[0].strip())
        else:
            return 0

    def getAbstractAuthor(self, author_list):
        if len(author_list) > 0:
            paper_author_out = "["
            for a in author_list:
                if len(a.strip()) > 0:
                    paper_author_out = paper_author_out + "{\"name\":\"%s\",\"org\":\"%s\"}," % (a, "")
            return paper_author_out.rstrip(',') + ']'
        else:
            return ""