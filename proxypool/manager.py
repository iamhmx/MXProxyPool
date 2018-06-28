from multiprocessing import Process
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.crawl import Crawler
from proxypool.api import start_api
from time import sleep
from proxypool.settings import *


class Manager(object):
    def handle_getter(self):
        """
        爬取代理
        """
        crawler = Crawler()
        client = RedisClient()
        while True:
            for proxy in crawler.start_crawl():
                client.add(proxy)
            sleep(20)

    def handle_tester(self):
        """
        测试代理
        """
        tester = Tester()
        while True:
            tester.run()
            sleep(20)

    def handle_api(self):
        """
        开启api
        """
        start_api()

    def start_pool(self):
        if ENABLE_CRAWL:
            process = Process(target=self.handle_getter)
            process.start()

        if ENABLE_TEST:
            process = Process(target=self.handle_tester)
            process.start()

        if ENABLE_API:
            process = Process(target=self.handle_api)
            process.start()


if __name__ == '__main__':
    m = Manager()
    m.start_pool()
