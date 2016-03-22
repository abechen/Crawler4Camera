# encoding=utf8
from scrapy import Spider
from scrapy.http import Request
from Crawler4Camera.items import Crawler4CameraItem
import datetime
import urlparse


class PhotoSharpSpider(Spider):
    name = "photosharp"
    allowed_domains = ["www.photosharp.com.tw/"]
    start_urls = ["http://www.photosharp.com.tw/KeyBuy/Index.aspx?PageNum=%d" % int(i+1) for i in range(0, 1)]

    def parse(self, response):
        items = []
        for sel in response.xpath('//*[@id="preview"]/tr[@class="content"]'):
            item = Crawler4CameraItem()
            item['source'] = 'photosharp'
            item['href'] = "www.photosharp.com.tw/KeyBuy/" + sel.xpath('td[3]/nobr/a/@href').extract()[0]
            self.logger.info('href => %s', item['href'])
            item['crawlDateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            items.append(item)

        for item in items:
            request = Request("http://" + item['href'], callback=self.parse_detail, dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        items = []
        item['title'] = response.xpath('//*[@id="Form1"]/table[3]/tr/td[1]/a[3]/text()').extract()[0]
        item['price'] = response.xpath('//*[@id="Price"]/text()').extract()[0]
        item['memberId'] = response.xpath('//*[@id="Form1"]/table[3]/tr/td[1]/a[4]/text()').extract()[0]
        item['memberName'] = ""
        item['articleId'] = ""
        item['location'] = response.xpath('//*[@id="AreaTD"]/nobr/text()').extract()[0]
        item['postDateTime'] = response.xpath('//*[@id="AreaTD"]/nobr/text()').extract()[0]
        #item['image_urls'] = [urlparse.urljoin(response.url, u) for u in response.xpath('//*[@id="ImageTD"]/img[1]/@src').extract() ]
        content = ''
        for c in response.xpath('//*[@id="Description"]/text()').extract():
            content = content + c.replace("\n", "").replace("<br/>", "").strip() + '|'
        item['content'] = content
        items.append(item)

        return items