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
        contents = {
          "type": "carousel",
          "contents": [
            {
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
                        "text": "香港药店",
                        "wrap": True,
                        "weight": "bold",
                        "size": "xxl"
                      },
                      {
                        "type": "text",
                        "text": "口罩",
                        "size": "xxl"
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
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl"
                      },
                      {
                        "type": "text",
                        "text": "$12 / 盒",
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
                        "text": "Quantity",
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl"
                      },
                      {
                        "type": "text",
                        "text": "34 盒",
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
                        "text": "2012/12/30 11:40:89",
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
                        "text": "杨高北路, Pudong Shanghai China",
                        "size": "lg"
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
                        }
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "postback",
                          "label": "Delete",
                          "data": "id"
                        },
                        "style": "primary",
                        "color": "#DC3545"
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
                        "color": "#007BFF"
                      }
                    ]
                  }
                ]
              }
            },
            {
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
                                      "text": "香港药店",
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xxl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "口罩",
                                      "size": "xxl"
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
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "$12 / 盒",
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
                                      "text": "Quantity",
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "34 盒",
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
                                      "text": "2012/12/30 11:40:89",
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
                                      "text": "杨高北路, Pudong Shanghai China",
                                      "size": "lg"
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
                                      }
                                  },
                                  {
                                      "type": "button",
                                      "action": {
                                          "type": "postback",
                                          "label": "Delete",
                                          "data": "id"
                                      },
                                      "style": "primary",
                                      "color": "#DC3545"
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
                                      "color": "#007BFF"
                                  }
                              ]
                          }
                      ]
                  }
              },
            {
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
                                      "text": "香港药店",
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xxl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "口罩",
                                      "size": "xxl"
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
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "$12 / 盒",
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
                                      "text": "Quantity",
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "34 盒",
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
                                      "text": "2012/12/30 11:40:89",
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
                                      "text": "杨高北路, Pudong Shanghai China",
                                      "size": "lg"
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
                                      }
                                  },
                                  {
                                      "type": "button",
                                      "action": {
                                          "type": "postback",
                                          "label": "Delete",
                                          "data": "id"
                                      },
                                      "style": "primary",
                                      "color": "#DC3545"
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
                                      "color": "#007BFF"
                                  }
                              ]
                          }
                      ]
                  }
              },
            {
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
                                      "text": "香港药店",
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xxl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "口罩",
                                      "size": "xxl"
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
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "$12 / 盒",
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
                                      "text": "Quantity",
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "34 盒",
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
                                      "text": "2012/12/30 11:40:89",
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
                                      "text": "杨高北路, Pudong Shanghai China",
                                      "size": "lg"
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
                                      }
                                  },
                                  {
                                      "type": "button",
                                      "action": {
                                          "type": "postback",
                                          "label": "Delete",
                                          "data": "id"
                                      },
                                      "style": "primary",
                                      "color": "#DC3545"
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
                                      "color": "#007BFF"
                                  }
                              ]
                          }
                      ]
                  }
              },
            {
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
                                      "text": "香港药店",
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xxl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "口罩",
                                      "size": "xxl"
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
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "$12 / 盒",
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
                                      "text": "Quantity",
                                      "wrap": True,
                                      "weight": "bold",
                                      "size": "xl"
                                  },
                                  {
                                      "type": "text",
                                      "text": "34 盒",
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
                                      "text": "2012/12/30 11:40:89",
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
                                      "text": "杨高北路, Pudong Shanghai China",
                                      "size": "lg"
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
                                      }
                                  },
                                  {
                                      "type": "button",
                                      "action": {
                                          "type": "postback",
                                          "label": "Delete",
                                          "data": "id"
                                      },
                                      "style": "primary",
                                      "color": "#DC3545"
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
                                      "color": "#007BFF"
                                  }
                              ]
                          }
                      ]
                  }
              },
          ]
        }
        return contents
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
        return "Data type error, need " + validate[self.__redis.hlen(InformationKey)] + ", please reply again"
    def __DeleteInformation(self):
        return
    def __ModifyInformation(self):
        return
    def __SearchInformation(self):
        return
    def __Comment(self):
        message = self.__message.split("-",2)
        informationID = message[1]
        comment = message[2]
        InformationKey = self.__redis.keys("Information:*:" + informationID)
        if len(InformationKey) != 1:
            return "No such record ID, please reply again"
        UserID = InformationKey[0].decode().split(":")[1]
        if UserID == self.__userid:
            return "Can't comment your own record, please reply again"
        CommentKey = "Comment:" + self.__userid + ":" + informationID
        self.__redis.set(CommentKey, comment)
        return "Comment successfully"
    def __Rate(self):
        message = self.__message.split("-", 2)
        informationID = message[1]
        rate = message[2]
        InformationKey = self.__redis.keys("Information:*:" + informationID)
        if len(InformationKey) != 1:
            return "No such record ID, please reply again"
        UserID = InformationKey[0].decode().split(":")[1]
        if UserID == self.__userid:
            return "Can't rate your own record, please reply again"
        # Validate Data Type
        try:
            int(rate)
            if int(rate) < 0 or int(rate) > 5:
                return "Range should from 0 to 5, please reply again"
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
