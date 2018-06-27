from proxypool.settings import *
import aiohttp
import asyncio
from proxypool.db import RedisClient
from time import sleep


class Tester(object):
    def __init__(self):
        self.client = RedisClient()

    async def test(self, proxy):
        """
        测试单个proxy
        :param proxy:
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                proxy_data = 'http://' + proxy
                async with session.get(TEST_URL, proxy=proxy_data, timeout=15) as response:
                    print('测试：%s，结果：%s' % (proxy_data, response.status))
                    if response.status in VALID_STATUS:
                        print('代理测试可用')
                        self.client.set_vaild(proxy)
                    else:
                        print('代理测试不可用，分值减一')
                        self.client.decrease(proxy)
            except Exception as e:
                print('测试失败', e, '分值减一')
                self.client.decrease(proxy)

    def run(self):
        """
        批量测试代理
        :return:
        """
        print('开始测试...')
        try:
            proxies = self.client.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), TEST_BATCH_SIZE):
                test_proxy = proxies[i:i+TEST_BATCH_SIZE]
                tester_list = [self.test(proxy) for proxy in test_proxy]
                loop.run_until_complete(asyncio.wait(tester_list))
                sleep(5)
        except Exception as e:
            print('测试发生错误', e)


if __name__ == '__main__':
    tester = Tester()
    tester.run()
