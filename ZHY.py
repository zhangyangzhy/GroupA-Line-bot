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
    def __ValidateDataType(self,validate):
        if validate == "Integer":
            try:
                int(self.__message)
                return True
            except ValueError:
                return False
        elif validate == "Float":
            try:
                float(self.__message)
                return True
            except:
                return False
        elif validate == "String":
            return True
        else:
            return False
    def __MyInformation(self):
        return
    def __PublishInformation(self):
        ActionKey = "Action:" + self.__userid
        InformationKey = "TempInformation:" + self.__userid
        EventKey = "NextEvent:" + self.__userid
        event = ["TextMessage","TextMessage","TextMessage","TextMessage","TextMessage","TextMessage","LocationMessage"]
        validate = ["String","String","String","Float","String","Integer","String"]
        attribute = ["Datetime","Store Name","Commodity Name","Price","Unit","Quantity","Location"]
        current = attribute[self.__redis.hlen(InformationKey)]
        # Validate Data Type
        if self.__ValidateDataType(validate[self.__redis.hlen(InformationKey)]):
            if self.__redis.hlen(InformationKey) == len(attribute)-1:
                self.__redis.delete(ActionKey)
                self.__redis.delete(EventKey)
                self.__redis.hset(InformationKey, current, self.__message)
                self.__redis.persist(InformationKey)
                # Guarantee each user can publish multiple information
                self.__redis.rename(InformationKey,"Information:"+self.__userid+":"+str(len(self.__redis.keys("Information:*"))+1))
                return "Publish information successfully"
            else:
                # Store next validate Event Type
                self.__redis.set(EventKey, event[self.__redis.hlen(InformationKey) + 1], ex=self.__expire)
                next = attribute[self.__redis.hlen(InformationKey) + 1]
                self.__redis.set(ActionKey, "#publish", ex=self.__expire)
                self.__redis.hset(InformationKey, current, int(time.time()) if self.__redis.hlen(InformationKey) == 0 else self.__message)
                self.__redis.expire(InformationKey, self.__expire)
                return "Please reply the " + next + " (" + event[self.__redis.hlen(InformationKey)] + "):"
        return "Data type error, need " + validate[self.__redis.hlen(InformationKey)] + ", please reply again:"
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
        self.__redis.delete("NextEvent:" + self.__userid)
        return "Procedure is over"
    def __Filter(self):
        key = "Action:"+self.__userid
        if self.__message == "#my":
            self.__redis.set(key, "#my", ex=self.__expire)
            return self.__MyInformation()
        elif self.__message == "#publish":
            # In case processing the same procedure again
            self.__Exit()
            return self.__PublishInformation()
        elif self.__message == "#search":
            self.__redis.set(key, "#search", ex=self.__expire)
            return self.__SearchInformation()
        elif self.__message.startswith("#delete-"):
            self.__redis.set(key, "#delete", ex=self.__expire)
            return self.__DeleteInformation()
        elif self.__message.startswith("#modify-"):
            self.__redis.set(key, "#modify", ex=self.__expire)
            return self.__ModifyInformation()
        elif self.__message.startswith("#comment-"):
            self.__redis.set(key, "#comment", ex=self.__expire)
            return self.__Comment()
        elif self.__message.startswith("#rate-"):
            self.__redis.set(key, "#rate", ex=self.__expire)
            return self.__Rate()
        elif self.__message == "#exit":
            return self.__Exit()
        else:
            if self.__redis.get(key) == b"#publish":
                return self.__PublishInformation()
            elif self.__redis.get(key) == b"#search":
                return self.__SearchInformation()
            elif self.__redis.get(key) == b"#delete":
                return self.__DeleteInformation()
            elif self.__redis.get(key) == b"#modify":
                return self.__ModifyInformation()
            else:
                return "Error!"
    def public(self,EventType):
        key = "NextEvent:" + self.__userid
        if self.__redis.exists(key):
            value = self.__redis.get(key).decode()
            if self.__message == "#exit":
                return self.__Exit()
            if EventType != value:
                return "Event type error, need " + value + ", please reply again (or you can reply #exit to end the current procedure)"
        return self.__Filter()
