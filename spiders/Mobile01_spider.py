# encoding=utf8
from scrapy import Spider
from scrapy.http import Request
from Crawler4Camera.items import Crawler4CameraItem
from bs4 import BeautifulSoup
import datetime


class Mobile01Spider(Spider):
    name = "mobile01"
    download_delay = 8
    allowed_domains = ["www.mobile01.com/"]
    start_urls = ['http://www.mobile01.com/mpcatlist.php?c=3&p=%d' % int(i+1) for i in range(0, 2)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        items = []
        for info in soup.select('.tablelist tr')[1:]:
            item = Crawler4CameraItem()
            item['source'] = 'mobile01'

            # 爬蟲抓取時間
            item['crawlDateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 賣家資訊
            try:
                item['memberId'] = info.select('div[class="subject"] a')[1]['href'].replace("mpitemlist.php?id=", "")
            except Exception as e:
                item['memberId'] = ""

            try:
                item['memberName'] = info.select('div[class="subject"] a')[1].get_text().encode('utf-8').strip()
            except Exception as e:
                item['memberName'] = ""

            try:
                item['href'] = 'www.mobile01.com/' + info.select('.subject .subject-text1')[0]['href'].replace("http://", "")
            except Exception as e:
                item['href'] = ""

            self.logger.info('href => %s', item['href'])

            try:
                item['articleId'] = item['href'].split('=')[1]
            except Exception as e:
                item['articleId'] = ""

            try:
                item['price'] = info.select('.price')[0].get_text().replace("  ", "").replace(",", "").replace(u"\u5143", "").strip()
            except Exception as e:
                item['price'] = ""

            #self.location = info.select('div[class="subject"]')[0].get_text().replace(u"\u9762\u4ea4", "").encode('utf-8').strip().split(':')[-1]
            try:
                item['postDateTime'] = info.find('div', class_='updated').text
            except Exception as e:
                item['postDateTime'] = ""

            items.append(item)

        # 取得子頁面資訊
        for item in items:
            request = Request("http://" + item['href'], callback=self.parse_detail, dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        items = []
        soup = BeautifulSoup(response.body, "lxml")

        try:
            item['title'] = soup.find('h2', class_='topic').text.encode('utf-8').strip()
        except Exception as e:
            item['title'] = ""

        try:
            item['content'] = soup.find('div', class_='single-post-content').text.encode('utf-8').strip()
        except Exception as e:
            item['content'] = ""

        try:
            item['location'] = soup.find('ul', class_='author-detail').text.encode('utf-8').split('交易地區:')[1].split('鄰')[0].strip()
        except Exception as e:
            item['location'] = ""

        items.append(item)

        return items