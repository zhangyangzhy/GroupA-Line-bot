import redis as redis


class NewsConnection:
    def __init__(self):
        self.__host = 'redis-17935.c1.ap-southeast-1-1.ec2.cloud.redislabs.com'
        self.__pwd = 'h79Y4ieXjngXsPESbT3KAPBVgGa8Hzhs'
        self.__port = '17935'

    def connect(self):
        return redis.Redis(host=self.__host, password=self.__pwd, port=self.__port, decode_responses=True)
