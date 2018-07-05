from pyquery import PyQuery as pq
from time import sleep
from proxypool.setuplogging import setup_logging
import logging

logger = logging.getLogger(__name__)


class CrawlerMetaclass(type):
    """
    元类，控制类行为
    """
    def __new__(cls, name, bases, attrs):
        """
        :param name: 类名 Crawler
        :param bases: 继承的父类 (<class 'object'>,)
        :param attrs: 属性及方法
        :return: 类
        """
        # print(name)
        # print(bases)
        # print(attrs)
        crawl_func_count = 0
        crawl_func_list = []
        for k, v in attrs.items():
            # 取出爬虫方法，方法名以crawl_开头
            if str(k).startswith('crawl_'):
                # print(k)
                crawl_func_count += 1
                crawl_func_list.append(k)
        # 添加到属性，Crawler实例可以直接访问
        attrs['__CrawlCount__'] = crawl_func_count
        attrs['__CrawlFunc__'] = crawl_func_list
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=CrawlerMetaclass):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.87 Safari/537.36'
        }

    def start_crawl(self):
        """
        调用所有爬虫方法：crawl_
        :return: 代理（ip+port）
        """
        # print(self.__CrawlCount__)
        # print(self.__CrawlFunc__)
        logger.info('开始爬取...')
        proxies = []
        for i in range(self.__CrawlCount__):
            func = self.__CrawlFunc__[i]
            for proxy in eval('self.{}()'.format(func)):
                proxies.append(proxy)
        return proxies

    def crawl_xici(self, page_count=10):
        """
        爬取xicidaili：http://www.xicidaili.com
        :param page_count:页数
        :return: 代理（ip+port）
        """
        base_url = 'http://www.xicidaili.com/nn/{}/'
        # 抓10页
        urls = [base_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            logger.info('爬取：%s', url)
            doc = pq(url=url, headers=self.headers)
            for tr in doc('#ip_list tr:gt(0)').items():
                yield tr('td:nth-child(2)').text() + ':' + tr('td:nth-child(3)').text()

    def crawl_kuaidaili(self, page_count=10):
        """
        爬取快代理：https://www.kuaidaili.com/free/inha/1/
        :param page_count:页数
        :return: 代理（ip+port）
        """
        base_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [base_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            logger.info('爬取：%s', url)
            doc = pq(url=url, headers=self.headers)
            for tr in doc('#list tbody tr').items():
                yield tr('td:nth-child(1)').text() + ':' + tr('td:nth-child(2)').text()
            sleep(2)

    def crawl_66ip(self):
        """
        爬取66ip：http://www.66ip.cn/
        先抓取地区url，再爬取每个地区页面上的代理
        :return: 代理（ip+port）
        """
        def get_page_url():
            start_url = 'http://www.66ip.cn'
            homepage_doc = pq(url=start_url, headers=self.headers)
            for li in homepage_doc('.textlarge22 li:gt(0)').items():
                href = li('a').attr('href')
                yield start_url + href
        for url in get_page_url():
            logger.info('爬取：%s', url)
            doc = pq(url=url, headers=self.headers)
            for tr in doc('#footer tr:gt(0)').items():
                yield tr('td:nth-child(1)').text() + ':' + tr('td:nth-child(2)').text()


if __name__ == '__main__':
    setup_logging()
    crawl = Crawler()
    # for proxy in crawl.crawl_kuaidaili(page_count=1):
    #     print(proxy)
    # print(crawl.__CrawlCount__)
    # print(crawl.__CrawlFunc__)
    proxies = crawl.start_crawl()
    logger.info(len(proxies))

