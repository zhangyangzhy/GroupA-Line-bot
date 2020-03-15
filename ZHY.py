import redis
import time
import datetime
import pytz
import json
import random
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
            except ValueError:
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
    def __GetComment(self):
        Informationid = self.__message
        CommentKey = self.__redis.keys("Comment:*:" + Informationid)
        if len(CommentKey) == 0:
            InformationKey = self.__redis.keys("Information:*:" + Informationid)
            if len(InformationKey) == 0:
                return "Not available because information has been deleted"
            else:
                return "No one comments this information"
        else:
            contents = "Comment of #"+Informationid+" Information:"
            for key in CommentKey:
                comment = self.__redis.get(key)
                contents = contents + "\n\n" + comment
            return contents
    def __MyInformation(self):
        InformationKey = self.__redis.keys("Information:" + self.__userid + ":*")
        if len(InformationKey) == 0:
            return "You haven't published information yet, try to reply #publish"
        else:
            contents = []
            for info in  InformationKey:
                key = info
                id = key.split(":")[-1]
                dic = self.__redis.hgetall(key)
                LatLng = json.loads(dic["Location"])["latlng"].split(",")
                lat = LatLng[0]
                lng = LatLng[1]
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
                                  "data": "Modify=%(i)s"
                                },
                                "height": "sm"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "postback",
                                  "label": "Delete",
                                  "data": "Delete=%(i)s&Step=1"
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
                                  "label": "Get Location",
                                  "data": "%(Location)s"
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
                                  "data": "%(Comment)s"
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
                    't':datetime.datetime.fromtimestamp(float(dic["Datetime"]), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
                    'a':json.loads(dic["Location"])["address"],
                    'Location':"Address="+str(json.loads(dic["Location"])["address"])+"&Lat="+str(lat)+"&Lng="+str(lng)+"&Title="+str(dic["Store Name"]),
                    'Comment':"GetComment="+id
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
                InformationId = str(int(time.time()))+str(random.randint(100,999))
                # Guarantee each user can publish multiple information
                self.__redis.rename(InformationKey,"Information:"+self.__userid+":"+InformationId)
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
        InformationId = self.__message
        UserId = self.__userid
        Informationkey = "Information:"+UserId+":"+InformationId
        CommentKeys = self.__redis.keys("Comment:*:"+InformationId)
        RateKeys = self.__redis.keys("Rate:*:"+InformationId)
        if self.__redis.exists(Informationkey):
            self.__redis.delete(Informationkey)
            for comment in CommentKeys:
                self.__redis.delete(comment)
            for rate in RateKeys:
                self.__redis.delete(rate)
            return "Delete successfully"
        else:
            return "Fail to delete, this information has been deleted before"
    def __ModifyInformation(self,step):
        attributes = ["Store Name", "Commodity Name", "Price", "Unit", "Quantity", "Location"]
        events = ["TextMessage", "TextMessage", "TextMessage", "TextMessage", "TextMessage","LocationMessage"]
        validates = ["String", "String", "Float", "String", "Integer", "String"]
        ActionKey = "Action:" + self.__userid
        EventKey = "NextEvent:" + self.__userid
        if step == 1:
            InformationKey = "Information:" + self.__userid + ":" + self.__message
            if self.__redis.exists(InformationKey):
                self.__redis.set(ActionKey, "#modify@"+self.__message, ex=self.__expire)
                self.__redis.set(EventKey, "TextMessage", ex=self.__expire)
                content = "Please reply one attribute:"
                for attribute in attributes:
                    content = content + "\n" + attribute
                return content
            else:
                return "Fail to modify, this information has been deleted before"
        elif step == 2:
            if self.__message in attributes:
                id = self.__redis.get(ActionKey).split("@")[1]
                index = attributes.index(self.__message)
                event = events[index]
                self.__redis.set(EventKey, event, ex=self.__expire)
                self.__redis.set(ActionKey, "#modify-"+id+"-"+self.__message, ex=self.__expire)
                return "Please reply the value of '" + self.__message + "':"
            else:
                return "Attribute name error, please reply again"
        else:
            split = self.__redis.get(ActionKey).split("-")
            id = split[1]
            attribute = split[2]
            index = attributes.index(attribute)
            InformationKey = "Information:" + self.__userid + ":" + id
            if self.__ValidateDataType(validates[index]):
                self.__redis.delete(ActionKey)
                self.__redis.delete(EventKey)
                self.__redis.hset(InformationKey, attribute, self.__message)
                # Update time after modification
                self.__redis.hset(InformationKey, "Datetime", time.time())
                return "Modify '"+ attribute +"' successfully"
            return "Data type error, need " + validates[index] + ", please reply again"
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
            return self.__MyInformation()
        elif self.__message == "#publish":
            # In case processing the same procedure again
            self.__Exit()
            return self.__PublishInformation()
        elif self.__message == "#search":
            self.__redis.set(key, "#search", ex=self.__expire)
            return self.__SearchInformation()
        elif str(self.__message).startswith("#comment-"):
            return self.__Comment()
        elif str(self.__message).startswith("#rate-"):
            return self.__Rate()
        elif self.__message == "#exit":
            return self.__Exit()
        else:
            if self.__redis.get(key) == "#publish":
                return self.__PublishInformation()
            elif self.__redis.get(key) == "#search":
                return self.__SearchInformation()
            elif str(self.__redis.get(key)).startswith("#modify"):
                if str(self.__redis.get(key)).startswith("#modify@"):
                    return self.__ModifyInformation(2)
                else:
                    return self.__ModifyInformation(3)
            else:
                return "Event type error!"
    def public(self,EventType):
        if EventType == "ModifyInformation":
            # In case processing the same procedure again
            self.__Exit()
            return self.__ModifyInformation(1)
        if EventType == "DeleteInformation":
            return self.__DeleteInformation()
        if EventType == "GetComment":
            return self.__GetComment()
        key = "NextEvent:" + self.__userid
        if self.__redis.exists(key):
            value = self.__redis.get(key)
            if self.__message == "#exit":
                return self.__Exit()
            if EventType != value:
                return "Event type error, need " + value + ", please reply again (or you can reply #exit to end the current procedure)"
        return self.__Filter()
