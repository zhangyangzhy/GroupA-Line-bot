import redis
import time
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
        self.__expire = 180
        self.__redis = Connection().connect()
    def __MyInformation(self):
        return
    def __PublishInformation(self):
        ActionKey = "Action:" + self.__userid
        InformationKey = "TempInformation:" + self.__userid
        attribute = ["Datetime","Store Name","Commodity Type","Live Picture","Price","Unit","Quantity","Location"]
        current = attribute[self.__redis.hlen(InformationKey)]
        if self.__redis.hlen(InformationKey) == len(attribute)-1:
            self.__redis.delete(ActionKey)
            self.__redis.hset(InformationKey, current, self.__message)
            self.__redis.persist(InformationKey)
            self.__redis.rename(InformationKey,"Information:" + self.__userid)
            return "Publish Information Successfully"
        else:
            next = attribute[self.__redis.hlen(InformationKey) + 1]
            self.__redis.set(ActionKey, "#Publish Information", ex=self.__expire)
            self.__redis.hset(InformationKey, current, int(time.time()) if self.__redis.hlen(InformationKey) == 0 else self.__message)
            self.__redis.expire(InformationKey, self.__expire)
            return "Please Reply " + next + ":"
    def __DeleteInformation(self):
        return
    def __ModifyInformation(self):
        return
    def __SearchInformation(self):
        return
    def __Comment(self):
        return
    def __Rate(self):
        return
    def __Exit(self):
        self.__redis.delete("Action:"+self.__userid)
        self.__redis.delete("TempInformation:" + self.__userid)
        return "Session is over"
    def filter(self):
        key = "Action:"+self.__userid
        if self.__message == "#My Information":
            self.__redis.set(key, "#My Information", ex=self.__expire)
            return self.__MyInformation()
        elif self.__message == "#Publish Information":
            return self.__PublishInformation()
        elif self.__message == "#Search Information":
            self.__redis.set(key, "#Search Information", ex=self.__expire)
            return self.__SearchInformation()
        elif self.__message.startswith("#Delete Information-"):
            self.__redis.set(key, "#Delete Information", ex=self.__expire)
            return self.__DeleteInformation()
        elif self.__message.startswith("#Modify Information-"):
            self.__redis.set(key, "#Modify Information", ex=self.__expire)
            return self.__ModifyInformation()
        elif self.__message.startswith("#Comment-"):
            self.__redis.set(key, "#Comment", ex=self.__expire)
            return self.__Comment()
        elif self.__message.startswith("#Rate-"):
            self.__redis.set(key, "#Rate", ex=self.__expire)
            return self.__Rate()
        elif self.__message == "#Exit":
            return self.__Exit()
        else:
            if self.__redis.get(key) == b"#Publish Information":
                return self.__PublishInformation()
            elif self.__redis.get(key) == b"#Search Information":
                return self.__SearchInformation()
            elif self.__redis.get(key) == b"#Delete Information":
                return self.__DeleteInformation()
            elif self.__redis.get(key) == b"#Modify Information":
                return self.__ModifyInformation()
            else:
                return "Please input action first"