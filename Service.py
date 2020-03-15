from __future__ import unicode_literals

import os
import sys
import redis

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookParser)
from linebot.exceptions import (InvalidSignatureError)

from linebot.models import (MessageEvent, TextMessage, TextSendMessage,
                            ImageMessage, VideoMessage, FileMessage,
                            StickerMessage, StickerSendMessage)
from linebot.utils import PY3

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# get redis_host, redis_password and redis_port from your environment variable
redis_host = os.getenv('REDIS_HOST', None)
redis_password = os.getenv('REDIS_PASSWORD', None)
redis_port = os.getenv('REDIS_PORT', None)

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

# connect the redis server
r = redis.Redis(host=redis_host, password=redis_password, port=redis_port)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

flag = 0
test_x = 0
test_y = 0
test_z = 0


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
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage(event)
        if isinstance(event.message, ImageMessage):
            handle_ImageMessage(event)
        if isinstance(event.message, VideoMessage):
            handle_VideoMessage(event)
        if isinstance(event.message, FileMessage):
            handle_FileMessage(event)
        if isinstance(event.message, StickerMessage):
            handle_StickerMessage(event)

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'


def basic_measure(event, flag):
    '''
    Basic test for user
    event: user input
    flag: question No. use as global variable.
    x, y, z: used for contain user's input, and compute the final score
    threshold: score threshold
    '''
    re_msg = [
        "Question 1: Have you been to the epidemic area in the past 14 days? 0(No)/1(Yes)",
        "Question 2: Have you been in contact with a suspected infected person in the past 14 days? 0(No)/1(Yes)",
        "Qeustion 3: Do you have fever, cough, or difficulty breathing? 0(No)/1(Yes)"
    ]
    weight = [0.2, 0.3, 0.5]
    threshold = 0.7
    print(flag)
    global test_x, test_y, test_z
    # enter the test part for the first time, output the first question
    if flag == 1:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(re_msg[0]))
    # the second time, recieve user's input -> int. Output the second question
    if flag == 2:
        test_x = int(str(event.message.text)[1])
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(re_msg[1]))
    # the third time, recieve the second answer,.Output the third question
    if flag == 3:

        test_y = int(str(event.message.text)[1])
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(re_msg[2]))
    # the fourth time, recieve the third answer, output the final report.
    if flag == 4:
        test_z = int(str(event.message.text)[1])
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


def handle_Text(event):
    print(event.message.text)
    msg = event.message.text
    ls = str(msg).lower().split(" ")
    print(ls)
    for i in ls:
        print(i)
        # if the key does not exist, return None.
        value = str(r.get(i))
        if value == "None":
            continue
        else:
            print(value)
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(value))


# Handler function for Text Message
def handle_TextMessage(event):
    global flag
    global test_x, test_y, test_z
    if event.message.text == "$basic measurements":
        flag += 1
        basic_measure(event, flag)
    else:
        if flag == 0:
            handle_Text(event)
        else:
            if flag == 3:
                flag += 1
                basic_measure(event, flag)
                # end of the test, reset the global variables
                flag = 0
                test_x, test_y, test_z = 0, 0, 0
            else:
                flag += 1
                basic_measure(event, flag)


# Handler function for Sticker Message
def handle_StickerMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(package_id=event.message.package_id,
                           sticker_id=event.message.sticker_id))


# Handler function for Image Message
def handle_ImageMessage(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text="Nice image!"))


# Handler function for Video Message
def handle_VideoMessage(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text="Nice video!"))


# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text="Nice file!"))


if __name__ == "__main__":
    arg_parser = ArgumentParser(usage='Usage: python ' + __file__ +
                                ' [--port <port>] [--help]')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)
