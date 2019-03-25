import random
import redis
from ProxyPool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from ProxyPool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
import re
from ProxyPool.error import PoolEmptyError


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: redis地址
        :param port: redis端口
        :param password: redis 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy:
        :param score:
        :return:
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def get_random_proxy(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return:
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return random.choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy:代理
        :return:修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MAX_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy:
        :return:
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy:
        :return:
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取数量
        :return:
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start:开始索引
        :param stop:结束索引
        :return:
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)
