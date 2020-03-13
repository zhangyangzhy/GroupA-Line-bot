import redis
class Connection:
    def __init__(self):
        self.__host = "redis-16887.c15.us-east-1-4.ec2.cloud.redislabs.com"
        self.__pwd = "xAm8g5NfhvWK6AJstknNJhsFg9M8YuRD"
        self.__port = "16887"
    def connect(self):
        return redis.Redis(host = self.__host, password = self.__pwd, port = self.__port)
class ProcessMessage:
    def __init__(self,userid,message):
        self.__userid = userid
        self.__message = message.strip()
        self.__expire = 60
        self.__redis = Connection().connect()
    def __MyInformation(self):
        return
    def __PublishInformation(self):
        return
    def __DeleteInformation(self):
        return
    def __ModifyInformation(self):
        return
    def __Location(self):
        return
    def __Comment(self):
        return
    def __Rate(self):
        return
    def filter(self):
        key = "Action:"+self.__userid
        if self.__message == "#My Information":
            self.__redis.set(key, "#My Information", ex=self.__expire)
            return self.__MyInformation()
        elif self.__message == "#Publish Information":
            self.__redis.set(key, "#Publish Information", ex=self.__expire)
            return self.__PublishInformation()
        elif self.__message.startswith("#Delete Information"):
            self.__redis.set(key, "#Delete Information", ex=self.__expire)
            return self.__DeleteInformation()
        elif self.__message.startswith("#Modify Information"):
            self.__redis.set(key, "#Modify Information", ex=self.__expire)
            return self.__ModifyInformation()
        elif self.__message.startswith("#Location"):
            self.__redis.set(key, "#Location", ex=self.__expire)
            print("Have another format")
            return self.__Location()
        elif self.__message.startswith("#Comment"):
            self.__redis.set(key, "#Comment", ex=self.__expire)
            return self.__Comment()
        elif self.__message.startswith("#Rate"):
            self.__redis.set(key, "#Rate", ex=self.__expire)
            return self.__Rate()
        elif self.__message == "#Exit":
            self.__redis.delete(key)
            return "Session is over"
        else:
            if self.__redis.exists(key):
                return "Get parameter ing..."
            else:
                return "Please input action first"