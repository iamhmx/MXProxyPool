from proxypool.manager import Manager
from proxypool.setuplogging import setup_logging


def main():
    try:
        # proxies = Crawler().start_crawl()
        # print('一共获取到：%s 条代理' % len(proxies))
        # for proxy in proxies:
        #     RedisClient().add(proxy)
        # start_api()
        m = Manager()
        m.start_pool()
    except:
        main()


if __name__ == '__main__':
    setup_logging()
    main()
