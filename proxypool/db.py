from redis import StrictRedis
from proxypool.settings import *
import random


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        连接Redis
        :param host: redis host
        :param port: 端口号
        :param password: redis密码
        """
        # Address already in use:
        # $ ps aux | grep redis
        # $ kill -9 xxx
        # $ redis-server
        self.client = StrictRedis(host=host, port=port, password=password)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理到redis
        :param proxy: 代理
        :return: 添加结果
        """
        if self.client.zscore(REDIS_KEY, proxy) is None:
            print('Redis不存在该数据，可插入')
            print('代理：{}，分值：{}'.format(proxy, score))
            return self.client.zadd(REDIS_KEY, score, proxy)
        else:
            print('已有该条数据')

    def set_vaild(self, proxy, score=MAX_SCORE):
        """
        设置分值
        :param proxy: 代理
        :return: 分值
        """
        self.client.zadd(REDIS_KEY, score, proxy)

    def decrease(self, proxy):
        """
        将代理分值减1，如果为0，删除该代理
        :param proxy: 代理
        :return:
        """
        score = self.client.zscore(REDIS_KEY, proxy)
        if score is not None:
            if score > 1:
                print('将 %s (当前分值：%s) 减1' % (proxy, score))
                self.client.zincrby(REDIS_KEY, proxy, -1)
            else:
                print('%s (当前分值：%s) 删除' % (proxy, score))
                self.client.zrem(REDIS_KEY, proxy)

    def count(self):
        """
        返回代理个数
        :return: 总数
        """
        return self.client.zcard(REDIS_KEY)

    def all(self):
        """
        取出所有代理
        :return: 所有代理
        """
        return self.client.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def get_score(self, proxy):
        """
        查看代理分值
        :param proxy: 代理
        :return: 分值
        """
        return self.client.zscore(REDIS_KEY, proxy)

    def random(self):
        """
        随机取一个代理，优先从高分值取
        :return: 代理
        """
        results = self.client.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(results):
            print('有%s个可用代理' % len(results))
            return random.choice(results)
        else:
            results = self.client.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(results) > 0:
                return random.choice(results)
            return None

    def clear(self):
        """
        清除Redis数据
        :return:
        """
        self.client.zremrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)


if __name__ == '__main__':
    client = RedisClient()
    # print('个数：', client.count())
    # print('插入')
    # client.add_proxy('123')
    # print('个数：', client.count())
    # print(client.all())
    # print('分数：', client.get_score('123'))
    # client.add_proxy('456')
    # print(client.all())
    # client.decrease('123')
    # print(client.all())
    # client.decrease('456')
    # client.add_proxy('111', 10)
    # client.add_proxy('222', 100)
    # client.add_proxy('333', 50)
    # client.add_proxy('444', 2)
    # client.add_proxy('555', 11)
    # print(client.all())
    # print(client.random())
    # client.add_proxy('777', 100)
    # print(client.random())
    # client.add('111', 10)
    # client.add('222', 100)
    # client.add('333', 50)
    # client.add('444', 2)
    # client.add('555', 11)
    # client.add('666', 100)
    # print(client.count())
    # proxy = client.random()
    # print('代理：', proxy, '分值：', client.get_score(proxy))
    print(client.get_score('222.175.73.14:8060'))
    print(client.random())
