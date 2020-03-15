from __future__ import unicode_literals

import os
import sys
import redis

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookParser)
from linebot.exceptions import (InvalidSignatureError)

from linebot.models import (FollowEvent, PostbackEvent, MessageEvent,
                            TextMessage, TextSendMessage, ImageMessage,
                            VideoMessage, FileMessage, StickerMessage,
                            StickerSendMessage, TemplateSendMessage,
                            ButtonsTemplate, PostbackAction, LocationMessage,
                            AudioMessage, QuickReplyButton, QuickReply,
                            BubbleContainer, FlexSendMessage, LocationSendMessage,ConfirmTemplate)
from linebot.utils import PY3
from ZHY import ProcessMessage
import json
from urllib import parse


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# get redis_host, redis_password and redis_port from your environment variable
redis_host = os.getenv('REDIS_HOST', None)
redis_password = os.getenv('REDIS_PASSWORD', None)
redis_port = os.getenv('REDIS_PORT', None)

r = redis.Redis(host=redis_host, password=redis_password, port=redis_port)

# connect the redis server --- Hubert's
redis_host_li = "redis-19723.c61.us-east-1-3.ec2.cloud.redislabs.com"
redis_password_li = "15235021453.ljhX"
redis_port_li = "19723"

r_li = redis.Redis(host=redis_host_li,
                   password=redis_password_li,
                   port=redis_port_li)

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if isinstance(event, FollowEvent):
            handle_FollowEvent(event)
        if isinstance(event, PostbackEvent):
            handle_PostbackEvent(event)
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage(event)
        if isinstance(event.message, LocationMessage):
            handle_LocationMessage(event)
        if isinstance(event.message, ImageMessage):
            handle_ImageMessage(event)
        if isinstance(event.message, VideoMessage):
            handle_VideoMessage(event)
        if isinstance(event.message, FileMessage):
            handle_FileMessage(event)
        if isinstance(event.message, AudioMessage):
            handle_AudioMessage(event)
        if isinstance(event.message, StickerMessage):
            handle_StickerMessage(event)

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'


# For Part 3
flag = 0
test_x = 0
test_y = 0
test_z = 0


# Handle self-test function for Part 3
def basic_measure(event):
    '''
    Basic test for user
    event: user input
    flag: question No. use as global variable.
    x, y, z: used for contain user's input, and compute the final score
    threshold: score threshold
    '''
    re_msg = [
        "Question 1: Have you been to the epidemic area in the past 14 days? $0(No)/$1(Yes)",
        "Question 2: Have you been in contact with a suspected infected person in the past 14 days? $0(No)/$1(Yes)",
        "Qeustion 3: Do you have fever, cough, or difficulty breathing? $0(No)/$1(Yes)"
    ]
    weight = [0.2, 0.3, 0.5]
    threshold = 0.7
    global flag
    print(flag)
    global test_x, test_y, test_z
    # enter the test part for the first time, output the first question
    if flag == 1:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(re_msg[0]))

    # the second time, recieve user's input -> int. Output the second question
    if flag == 2:
        # input value start with $
        test_x = int(str(event.message.text)[1])
        print(test_x)
        if test_x == 0 or test_x == 1:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(re_msg[1]))
        else:
            flag = 1
            print("changed flag when wrong{}".format(flag))
            test_x, test_y, test_z = 0, 0, 0
            war_msg = "You input the wrong integer. Please follow the instructions. Thanks!"
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(war_msg))

    # the third time, recieve the second answer,.Output the third question
    if flag == 3:
        test_y = int(str(event.message.text)[1])
        if test_y == 0 or test_y == 1:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(re_msg[2]))
        else:
            flag = 2
            test_y, test_z = 0, 0
            war_msg = "You input the wrong integer. Please follow the instructions. Thanks!"
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(war_msg))
    # the fourth time, recieve the third answer, output the final report.
    if flag == 4:
        test_z = int(str(event.message.text)[1])
        if test_z == 0 or test_z == 1:
            # calculate the final score
            score = weight[0] * test_x + weight[1] * test_y + weight[2] * test_z
            # if the score >= threshold, return high risk
            if score >= threshold:
                report = "Based on your description, we suggest you are at higher risk, please go to the hospital for a diagnosis."
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(report))
            # if 0 < score < threshold, return quaratine.
            elif 0 < score < threshold:
                report = "Based on your description, we highly suggest that you quarantine for 14 days."
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(report))
            # if score == 0, return healthy
            else:
                report = "Based on your description, we think you are healthy, but please wear a mask."
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(report))
        else:
            flag = 3
            print("第三个问题错误{}".format(flag))
            test_z = 0
            war_msg = "You input the wrong integer. Please follow the instructions. Thanks!"
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(war_msg))


# Handle normal input
def handle_Text(event):
    '''
    handle Normal questions
    '''
    print(event.message.text)
    msg = event.message.text
    ls = str(msg).lower().strip().split(" ")
    print(ls)
    for i in range(len(ls)):
        print(ls[i])
        # if the key does not exist, return None.
        value = str(r_li.get(ls[i]))
        if value != "None":
            value = str(r_li.get(ls[i]))[2:-1]
            print(value)
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(value))

        # skip the word if iteration is not touch the len(ls)
        elif value == "None" and i + 1 < len(ls):
            continue
        # return 'not found' when searched whole sentence with nothing.
        elif value == "None" and i + 1 == len(ls):
            war_msg = "Try to find your query, but nothing return. You can try to input '$coronavirus', '$symptoms', '$measurements' or '$basic measurements' for query. :)"
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(war_msg))


# Handler function for Follow Event
def handle_FollowEvent(event):
    button_template_message = ButtonsTemplate(
        thumbnail_image_url=
        "https://obs.line-scdn.net/0h_TFUioZ5AHt7LCh0KO1_LFpxCxlITh5wWUpIGVwkXE1RHEBDExhPHg0sWhwBT0AuT0gbHjAsVh5XFUQrQA9OTg4pV09fGw/f256x256",
        title='Module List',
        text='Welcome to follow, click one to get the module instruction:',
        image_size="contain",
        actions=[
            PostbackAction(label='Publish & Search',
                           data='#Module 1 Instruction'),
            PostbackAction(label='News Summaries', data='#Module 2 Instruction'),
            PostbackAction(label='Anti-Coronavirus',
                           data='#Module 3 Instruction'),
        ])
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(alt_text="The Module Instruction",
                            template=button_template_message))


# Handler function for Postback Event
def handle_PostbackEvent(event):
    if event.postback.data == "#Module 1 Instruction":
        msg =TextSendMessage( '''Module 1 Instruction:

1. Reply '#my' to find the historical store information that you have published;

2. Reply '#publish' to publish the information;

3. Reply '#search' to query the records within 10KM of your current location;

4. Reply '#delete-ID' to delete the specific record you have published permanently;

5. Reply '#modify-ID' to modify the attribute value;

6. Reply '#comment-ID-CONTENT' to comment on store information that is not published by yourself;

7. Reply '#rate-ID-SCORE' to rate the credibility of store information;

8. Reply '#exit' to terminate the current procedure.''')
    elif event.postback.data == "#Module 2 Instruction":
        msg = TextSendMessage('''Module 2 Instruction:
TO DO...
Written by WU Peicong''')
    elif event.postback.data == "#Module 3 Instruction":
        msg = TextSendMessage('''Module 3 Instruction:

1. Reply '$measurements' to show information stored in the redis;

2. Reply '$symptoms' to return the symptoms of Coronavirus;

3. Reply '$coronavirus' to return general concept of Coronavirus;

4. Reply '$basic measurements' to provide a simple self-test for user.

Important:
Notice: You should add '$' at the beginning of your query when you want to test on this module. Thanks for cooperation. :)''')
    elif str(event.postback.data).startswith("Address="):
        params = parse.parse_qs(event.postback.data)
        msg = LocationSendMessage(
            title=params["Title"][0],
            address=params["Address"][0],
            latitude=params["Lat"][0],
            longitude=params["Lng"][0]
        )
    elif str(event.postback.data).startswith("GetComment="):
        params = parse.parse_qs(event.postback.data)
        message = ProcessMessage(event.source.user_id,params["GetComment"][0]).public("GetComment")
        msg = TextSendMessage(message)
    elif str(event.postback.data).startswith("Delete="):
        params = parse.parse_qs(event.postback.data)
        id = params["Delete"][0]
        step = params["Step"][0]
        if step == "1":
            msg = TemplateSendMessage(
                alt_text='Confirm Message',
                template=ConfirmTemplate(
                    text='Are you sure to delete?',
                    actions=[
                        PostbackAction(
                            label='Yes',
                            data='Delete='+id+'&Step=2'
                        ),
                        PostbackAction(
                            label='No',
                            data='Delete='+id+'&Step=3',
                        )
                    ]
                )
            )
        elif step == "2":
            message = ProcessMessage(event.source.user_id, id).public("DeleteInformation")
            msg = TextSendMessage(message)
        else:
            msg = TextSendMessage("Cancel successfully")
    elif str(event.postback.data).startswith("Modify="):
        params = parse.parse_qs(event.postback.data)
        id = params["Modify"][0]
        message = ProcessMessage(event.source.user_id, id).public("ModifyInformation")
        msg = TextSendMessage(message)
    else:
        msg = TextSendMessage("Error")
    line_bot_api.reply_message(event.reply_token, msg)


# Handler function for Text Message
def handle_TextMessage(event):
    if str(event.message.text).startswith("@"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("TO DO... Written by WU Peicong"))
    elif str(event.message.text).startswith("$"):
        global flag
        global test_x, test_y, test_z
        if event.message.text == "$basic measurements":
            if flag == 4:
                flag = 1
                basic_measure(event)
            else:
                flag += 1
                basic_measure(event)
        else:
            if flag == 0:
                handle_Text(event)
            else:
                if flag == 4:
                    # end of the test, reset the global variables
                    flag = 0
                    test_x, test_y, test_z = 0, 0, 0
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage("Please input again."))
                else:
                    flag += 1
                    basic_measure(event)
    else:
        message = ProcessMessage(event.source.user_id,
                                 event.message.text).public("TextMessage")
        if isinstance(message, dict):
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='My Published Information', contents=message))
        else:
            if message == "Event type error!":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text=
                        'Input error, reason:\n\n1. No action detected (tap quick reply for details);\n\n2. No response of previous action for long time.',
                        quick_reply=QuickReply(items=[
                            QuickReplyButton(action=PostbackAction(
                                label='Publish & Search',
                                data='#Module 1 Instruction')),
                            QuickReplyButton(action=PostbackAction(
                                label='News Summaries',
                                data='#Module 2 Instruction')),
                            QuickReplyButton(action=PostbackAction(
                                label='Anti-Coronavirus',
                                data='#Module 3 Instruction'))
                        ])))
            else:
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(message))


# Handler function for Location Message
def handle_LocationMessage(event):
    dic = {
        "latlng":
        str(event.message.latitude) + "," + str(event.message.longitude),
        "address": event.message.address
    }
    text = json.dumps(dic)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            ProcessMessage(event.source.user_id,
                           text).public("LocationMessage")))


# Handler function for Sticker Message
def handle_StickerMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            ProcessMessage(event.source.user_id,
                           event.message.id).public("StickerMessage")))


# Handler function for Image Message
def handle_ImageMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            ProcessMessage(event.source.user_id,
                           event.message.id).public("ImageMessage")))


# Handler function for Video Message
def handle_VideoMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            ProcessMessage(event.source.user_id,
                           event.message.id).public("VideoMessage")))


# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            ProcessMessage(event.source.user_id,
                           event.message.id).public("FileMessage")))


# Handler function for Audio Message
def handle_AudioMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            ProcessMessage(event.source.user_id,
                           event.message.id).public("AudioMessage")))


if __name__ == "__main__":
    arg_parser = ArgumentParser(usage='Usage: python ' + __file__ +
                                ' [--port <port>] [--help]')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)
