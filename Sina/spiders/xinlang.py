# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from Sina import items

class XinlangSpider(scrapy.Spider):
    name = 'xinlang'

    def start_requests(self):
        f = open('D:\ZHiYin\Sina\ID.txt')
        f.readline()
        for ids in f:
            print(ids)
            for num in range(7, 101):
                url = 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol={0}&Page={1}'.format(ids.strip(), num)
                yield Request(url, meta={'ids':ids})

    def parse(self, response):
        bea = BeautifulSoup(response.text, 'lxml')
        try:
            name = bea.find('h1', id="stockName").text.split('(')[0]
            urls = bea.find('div', 'datelist').find('ul').find_all('a')
            for i in urls:
                print(name)
                yield Request(i['href'],callback=self.get_con, dont_filter=False ,meta={'name':name,'ids': response.meta['ids']})
        except Exception as e:
            print(e)

    def get_con(self, response):
        item = items.SinaItem()
        urls = response.url
        name = response.meta['name']
        ids = response.meta['ids']
        bea = BeautifulSoup(response.text, 'lxml')
        try:
            title = bea.find('h1', id="artibodyTitle")
            if title == None:
                title = bea.find('h1')
            datatime = bea.find('span', 'date')
            if datatime == None:
                datatime = bea.find('span', 'time-source')
                if datatime == None:
                    datatime = bea.find('span', id="pub_date")
            data_str = datatime.text.replace('年', '-').replace('月', '-').replace('\n', '').replace('		    ', '').split(
                    '日')[0]
            content = bea.find('div', id="artibody").find_all('p')
            # print(ids)
            # print(name)
            # print(urls)
            # print(title.text)
            # print(data_str)
            contents = ''
            for con in content:
                contents += con.text + '\n'
            # print(contents)
            item['name'] = name
            item['ids'] = ids
            item['data_str'] = data_str
            item['title'] = title.text
            item['contents'] = contents
            item['urls'] = urls
            # item['type'] = 'A股'
            yield item
        except Exception as e:
            print(e)

