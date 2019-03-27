from redis import StrictRedis
from Weixin.config import *
from Weixin.request import WeixinRequest
from pickle import dumps, loads


class RedisQueue(object):
    def __init__(self):
        """
        初始化redis
        """
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def add(self, request):
        """
        向队列添加序列化后的Request
        :param request:
        :return:
        """
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        else:
            return False

    def pop(self):
        """
        取出下一个Request并反序列化
        :return:
        """
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def clear(self):
        self.db.delete(REDIS_KEY)

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0


if __name__ == '__main__':
    db = RedisQueue()
    start_url = 'http://www.baidu.com'
    weixin_request = WeixinRequest(url=start_url, callback='hello', need_proxy=True)
    db.add(weixin_request)
    request = db.pop()
    print(request)
    print(request.callback, request.need_proxy)
