# Scrapy settings for mapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mapper'

SPIDER_MODULES = ['mapper.spiders']
NEWSPIDER_MODULE = 'mapper.spiders'

DOWNLOAD_DELAY = 0.25

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mapper (+http://www.yourdomain.com)'
