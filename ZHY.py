import redis
import time
import json
class Connection:
    def __init__(self):
        self.__host = "redis-16887.c15.us-east-1-4.ec2.cloud.redislabs.com"
        self.__pwd = "xAm8g5NfhvWK6AJstknNJhsFg9M8YuRD"
        self.__port = "16887"
    def connect(self):
        return redis.Redis(host = self.__host, password = self.__pwd, port = self.__port, decode_responses=True)
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
    def __GetRate(self,id):
        InformationKey = self.__redis.keys("Rate:*:" + id)
        if len(InformationKey) > 0:
            sum = 0
            for rate in InformationKey:
                sum = sum + int(self.__redis.get(rate))
            return sum/len(InformationKey)
        return "No rate yet"
    def __MyInformation(self):
        InformationKey = self.__redis.keys("Information:" + self.__userid + ":*")
        if len(InformationKey) == 0:
            return "You haven't published information yet"
        else:
            contents = []
            for info in  InformationKey:
                key = info
                id = key.split(":")[-1]
                dic = self.__redis.hgetall(key)
                content = json.dumps({
                      "type": "bubble",
                      "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "%(s)s",
                                "weight": "bold",
                                "size": "xl"
                              },
                              {
                                "type": "text",
                                "text": "%(c)s",
                                "size": "xl"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "ID",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#F0AD4E"
                                },
                                {
                                    "type": "text",
                                    "text": "%(i)s",
                                    "size": "lg",
                                    "color": "#F0AD4E"
                                }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                "type": "text",
                                "text": "Rate",
                                "weight": "bold",
                                "size": "lg"
                              },
                              {
                                "type": "text",
                                "text": "%(r)s",
                                "size": "lg"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                "type": "text",
                                "text": "Price",
                                "weight": "bold",
                                "size": "lg"
                              },
                              {
                                "type": "text",
                                "text": "$%(p)s / %(u)s",
                                "size": "lg"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                "type": "text",
                                "text": "Quantity",
                                "weight": "bold",
                                "size": "lg"
                              },
                              {
                                "type": "text",
                                "text": "%(q)s %(u)s",
                                "size": "lg"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                "type": "text",
                                "text": "%(t)s",
                                "size": "md"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                "type": "text",
                                "text": "%(a)s",
                                "size": "md"
                              }
                            ]
                          }
                        ]
                      },
                      "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                "type": "button",
                                "style": "primary",
                                "action": {
                                  "type": "postback",
                                  "label": "Modify",
                                  "data": "id"
                                },
                                "height": "sm"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "postback",
                                  "label": "Delete",
                                  "data": "id"
                                },
                                "style": "primary",
                                "color": "#DC3545",
                                "height": "sm"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "button",
                                "action": {
                                  "type": "postback",
                                  "label": "Location",
                                  "data": "id"
                                },
                                "style": "primary",
                                "color": "#007BFF",
                                "height": "sm"
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "button",
                                "action": {
                                  "type": "postback",
                                  "label": "Check Comment",
                                  "data": "id"
                                },
                                "style": "link",
                                "height": "sm"
                              }
                            ]
                          }
                        ]
                      }
                    }) % {'s':dic["Store Name"],
                    'c':dic["Commodity Name"],
                    'i':id,
                    'r': self.__GetRate(id),
                    'p':dic["Price"],
                    'u':dic["Unit"],
                    'q':dic["Quantity"],
                    't':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(dic["Datetime"]))),
                    'a':json.loads(dic["Location"])["address"]
                }
                contents.append(json.loads(content))
            config = {
              "type": "carousel",
              "contents": contents
            }
            return config
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
                self.__redis.hset(InformationKey, current, time.time() if self.__redis.hlen(InformationKey) == 0 else self.__message)
                self.__redis.expire(InformationKey, self.__expire)
                return "Please reply the " + next + " (" + event[self.__redis.hlen(InformationKey)] + "):"
        return "Data type error, need " + validate[self.__redis.hlen(InformationKey)] + ", please reply again"
    def __DeleteInformation(self):
        return
    def __ModifyInformation(self):
        return
    def __SearchInformation(self):
        return
    def __Comment(self):
        message = self.__message.split("-",2)
        if len(message) != 3:
            return "Format error, should be #comment-ID-CONTENT, please reply again"
        informationID = message[1]
        if not informationID.isdigit():
            return "Record ID data type error, should be integer, please reply again"
        comment = message[2]
        if comment == "":
            return "Not allow empty comment, please reply again"
        InformationKey = self.__redis.keys("Information:*:" + informationID)
        if len(InformationKey) != 1:
            return "No such record ID, please reply again"
        UserID = InformationKey[0].split(":")[1]
        if UserID == self.__userid:
            return "Can't comment your own record, please reply again"
        CommentKey = "Comment:" + self.__userid + ":" + informationID
        self.__redis.set(CommentKey, comment)
        return "Comment successfully"
    def __Rate(self):
        message = self.__message.split("-", 2)
        if len(message) != 3:
            return "Format error, should be #rate-ID-SCORE, please reply again"
        informationID = message[1]
        if not informationID.isdigit():
            return "Record ID data type error, should be integer, please reply again"
        rate = message[2]
        if rate == "":
            return "Not allow empty score, please reply again"
        InformationKey = self.__redis.keys("Information:*:" + informationID)
        if len(InformationKey) != 1:
            return "No such record ID, please reply again"
        UserID = InformationKey[0].split(":")[1]
        if UserID == self.__userid:
            return "Can't rate your own record, please reply again"
        # Validate Data Type
        try:
            int(rate)
            if int(rate) < 0 or int(rate) > 100:
                return "Range should from 0 to 100, please reply again"
            RateKey = "Rate:" + self.__userid + ":" + informationID
            self.__redis.set(RateKey, rate)
            return "Rate successfully"
        except ValueError:
            return "Data type error, need Integer, please reply again"
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
            return self.__Comment()
        elif self.__message.startswith("#rate-"):
            return self.__Rate()
        elif self.__message == "#exit":
            return self.__Exit()
        else:
            if self.__redis.get(key) == "#publish":
                return self.__PublishInformation()
            elif self.__redis.get(key) == "#search":
                return self.__SearchInformation()
            elif self.__redis.get(key) == "#delete":
                return self.__DeleteInformation()
            elif self.__redis.get(key) == "#modify":
                return self.__ModifyInformation()
            else:
                return "Error!"
    def public(self,EventType):
        key = "NextEvent:" + self.__userid
        if self.__redis.exists(key):
            value = self.__redis.get(key)
            if self.__message == "#exit":
                return self.__Exit()
            if EventType != value:
                return "Event type error, need " + value + ", please reply again (or you can reply #exit to end the current procedure)"
        return self.__Filter()
