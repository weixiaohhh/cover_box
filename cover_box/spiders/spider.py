# coding:utf8
import scrapy
from scrapy.loader import ItemLoader 
from cover_box.items import CoverBoxItem,ImageItem
import re
import requests
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #允许打印unicode字符

class MyCoverSpider(scrapy.Spider):
    name = 'cover'
    allowed_domains = ['http://coverbox.sinaapp.com/']
    headers = {
        'host':'coverbox.sinaapp.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Referer': 'http://coverbox.sinaapp.com/?input=beatles&submit=%E6%8F%90%E4%BA%A4%E6%9F%A5%E8%AF%A2'
        }
    def __init__(self,cover_name=None, *args, **kwargs):
        super(MyCoverSpider, self).__init__(*args, **kwargs)
        self.cover_name = cover_name
    

    def start_requests(self):
        

         # 正则获取JavaScript中的信息
        payload = {'input':urllib.quote(unicode(self.cover_name, 'gbk').encode('utf8')),#转换成url 编码 格式的
        'submit':'%E6%8F%90%E4%BA%A4%E6%9F%A5%E8%AF%A2'}
        # 编码太坑爹了,requests抓取最好用content，然后解码
        r=requests.post('http://coverbox.sinaapp.com/list',data=payload,headers=self.headers).content.decode('UTF-8')
 
        artistName = r'"artistName":"(.*?)"'
        collectionName = r'"collectionName":"(.*?)"'
        artistViewUrl = r'"artistViewUrl":"(.*?)"'
        store = r'"collectionViewUrl":"(.*?)"'
        input = r'"artworkUrl100":"(.*?)"'
        collectionPrice = '"collectionPrice":(.*?),'
        releaseDate = '"releaseDate":(.*?),'


        artistName_list = re.findall(artistName,r)
        
        collectionName_list = re.findall(collectionName,r)

        artistViewUrl_list =re.findall(artistViewUrl,r)
        store_list = re.findall(store,r)

        input_list = re.findall(input,r)
        print input_list
        collectionPrice_list = re.findall(collectionPrice,r)
        releaseDate_list = re.findall(releaseDate,r)

        item = CoverBoxItem()
        zipped = zip(artistName_list, collectionName_list, artistViewUrl_list,
                        store_list, input_list, collectionPrice_list, releaseDate_list)
        for i in range(len(artistName_list)):

            # item['artistName'] = info[0]
            # item['collectionName'] = info[1]
            # item['artistViewUrl'] = info[2]
            # item['store'] = info[3]
            # item['input'] = info[4]
            # item['collectionPrice'] = info[5]
            # item['releaseDate'] = info[6]
            # yield item

            # post
            
            payload = {'input':input_list[i],
                'store':store_list[i],
                'way':'smart'}
            request = scrapy.FormRequest("http://coverbox.sinaapp.com/result",
                            formdata = payload,
                            headers=self.headers,
                            callback = self.Myparse,
                            dont_filter=True)
            request.meta['artistName'] = artistName_list[i]
            request.meta['collectionName'] = collectionName_list[i]
            yield request
        
 



            
    def Myparse(self, response):
        item = ImageItem()
        XL = response.xpath("//*[@id='XL']/@href").extract()[0]
        large = response.xpath("//*[@id='large']/@href").extract()[0]
        medium = response.xpath("//*[@id='medium']/@href").extract()[0]
        small = response.xpath("//*[@id='small']/@href").extract()[0]
        item['image_urls'] = [XL,large,medium,small]
        item['Band'] = self.cover_name
        item['collectionName'] = response.meta['collectionName']

        return item
        

	
    # def parse_item(self, response):
        # il = ItemLoader(item=ImageItem(), response=response)
        # il.add_css('image_urls', 'img::attr(src)')
        # return il.load_item()

    def errback(self, failure):
        pass