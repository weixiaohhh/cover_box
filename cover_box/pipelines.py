# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re    
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline

from scrapy.exceptions import DropItem

import json
import codecs

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('logo.json', 'w', encoding='utf-8')
    #当运行scrapy crawl logo -o items.json后,数据默认保存为items.json,里面中文全为Unicode,重新打开或创建一个文件'logo.json',名称随意

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()



class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url,meta={'item':item}) #添加meta是为了下面重命名文件名使用


    def file_path(self, request, response=None, info=None):
        item=request.meta['item'] #通过上面的meta传递过来item
        # 去掉空格，否则无法生成路径
        collectionName =  re.sub(' ','_',item['collectionName'])

        # 避免中文查询
        band = unicode(item['Band'], 'gbk')

        #图片文件名，item['collectionName']+xxx.jpg命名来四中不同大小的图片
        image_guid = collectionName+'~'+request.url.split('/')[-1]
        #图片下载目录 
        filename = u'full/{}/{}/{}'.format(band,collectionName,image_guid)

        return filename
 
        
    def item_completed(self, results, item, info):  
        image_paths = [x['path'] for ok, x in results if ok] 
 
        if not image_paths:  
            raise DropItem("Item contains no images")  
        return item 