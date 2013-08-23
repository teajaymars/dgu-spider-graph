from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from w3lib.url import url_query_cleaner
from scrapy.spider import BaseSpider
from scrapy.http import Request
from mapper.items import DgukSurveyItem

def url_cleaner(url):
    url = url_query_cleaner(url)
    url = url.replace('://www','://')
    return url

class DguliveSpider(BaseSpider):
    name = 'dgulive'
    allowed_domains = ['data.gov.uk']
    start_urls = ['http://data.gov.uk/']
    blocked = [
        # Dont open cached resources
        r'.*resource_cache.*',
        r'.*@[0-9:-\\.T]',
        r'data.gov.uk/api',
        r'\.csv$',
        r'\.rss$',
        r'\.atom$',
        r'data.gov.uk/data/',
        r'data.gov.uk/dataset/',
        r'data.gov.uk/data/site-usage/dataset/',
        r'data.gov.uk/harvest/gemini-object/',
        r'data.gov.uk/dataset/.*/resource/',
        r'data.gov.uk/dataset/.*/resource/',
        r'data.gov.uk/dataset/history/',
        r'data.gov.uk/flag/',
        r'data.gov.uk/flag/',
        r'\.data.gov.uk',
            ]
    sublinks = SgmlLinkExtractor( allow_domains='data.gov.uk', deny=blocked, process_value=url_cleaner  )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        i = DgukSurveyItem()
        title = hxs.select('//h1') or hxs.select('//h2')
        if title:
            title = title[0].extract()
        else:
            title = '(no title found)'
        local_links   = [ {'text':x.text,'url':x.url} for x in SgmlLinkExtractor(allow_domains='data.gov.uk').extract_links(response) ]
        offsite_links = [ {'text':x.text,'url':x.url} for x in SgmlLinkExtractor(deny_domains='data.gov.uk').extract_links(response) ]

        body_class = hxs.select('//body/@class').extract()
        if body_class and len(body_class):
            body_class = sorted(body_class[0].split())
        else: 
            body_class = ''
        # --
        i['url'] = response.url
        i['title'] = title
        i['local_links'] = local_links
        i['offsite_links'] = offsite_links
        i['body_class'] = body_class
        yield i
        for link in self.sublinks.extract_links(response):
            yield Request(url = link.url, callback=self.parse)
