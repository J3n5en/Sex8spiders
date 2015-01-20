__author__ = 'J3n5en'
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from sex8.items import Sex8Item
import os.path

try:
    import urllib.request
    # import urllib.parse
except ImportError:
    import urllib
    urllib.request = __import__('urllib2')
    urllib.parse = __import__('urlparse')

urlopen = urllib.request.urlopen
request = urllib.request.Request


def get_valid_filename(filename):
    keepcharacters = (' ', '.', '_')
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()


def down_link(url, filename, thresold = 0):
    if os.path.exists(filename) and os.path.getsize(filename) > 0: #TODO MD5
        return
    # filename = get_valid_filename(filename)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
    req = request(url, headers=headers)
    try:
        data = get_data_from_req(req)
        if data is '':
            return
        f = open(filename, 'wb')
        f.write(data)
        f.close
    except Exception as e:
        print(e)
    return


def get_data_from_req(req):
    attempts = 0
    binary = ''
    while attempts < 10:
        try:
            binary = urlopen(req).read()
            break
        except Exception as e:
            attempts += 1
            print(e)
    return binary


class Sex8Spider(CrawlSpider):

    name = 'sex8'
    # allowed_domains = ['mininova.org']
    start_urls = []
    for i in range(1, 30):
        start_urls.append('http://205.164.17.84/thread-htm-fid-280-page-%d.html' % i)
    # http://205.164.17.84/read-htm-tid-4606496-fpage-5.html
    rules = [Rule(LinkExtractor(allow=['http://205.164.17.84/read-htm-tid-\d+-fpage-\d.html']), 'f4ck_sex8')]

    def f4ck_sex8(self, response):
        info = Sex8Item()
        info['url'] = response.url
        name1 = ''.join(response.xpath("//div[@class='right_con']/a/font/text()").extract())
        info['name'] = name1.replace(".torrent", "")
        info['imgs'] = response.xpath("//div[@id='read_tpc']/img/@src").extract()
        info['torrent'] = "http://205.164.17.84/"+''.join(response.xpath("//div[@class='right_con']/a/@href").extract())

        if not os.path.exists("jensen/"+info['name']):
            os.makedirs("jensen/"+info['name'])
        down_link(info['torrent'], "jensen/"+info['name']+"/"+"F4ck.torrent")
        f4ckphoto = 1
        for img in info['imgs']:
            f4ckphoto += 1
            down_link(img, "jensen/"+info['name']+"/"+os.path.basename(img))
        return info
