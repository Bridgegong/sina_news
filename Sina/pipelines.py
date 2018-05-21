# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class SinaPipeline(object):
    def process_item(self, item, spider):
        # self.conn = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="zhiyin",use_unicode=True, charset="utf8")
        self.conn = pymysql.connect(host="192.168.20.143", port=3306, user="kg", password="kg", database="kg",
                                    use_unicode=True, charset="utf8")

        self.cur = self.conn.cursor()
        if self.cur:
            print("连接成功")
        else:
            print("连接失败")
        sql = "insert into sina_news(`Name`,NameID,`Data`,Title,Content,Url,Type) VALUES ('%s','%s','%s','%s','%s','%s', '%s')" % (
        item['name'], item['ids'], item['data_str'], item['title'], item['contents'], item['urls'], 'A股')
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        return item
