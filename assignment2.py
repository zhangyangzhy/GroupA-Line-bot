from __future__ import unicode_literals

import os
import sys
import redis

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, FileMessage, StickerMessage, StickerSendMessage, VideoSendMessage, ImageSendMessage
)
from linebot.utils import PY3

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

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

# Handler function for Text Message
def handle_TextMessage(event):
    print(event.message.text)
    msg = 'You have said: "' + event.message.text + '" ' + str(count_TextMessage(event.message.text)) + ' times.'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
    )

# Count text message
def count_TextMessage(msg):
    HOST = "redis-16887.c15.us-east-1-4.ec2.cloud.redislabs.com"
    PWD = "xAm8g5NfhvWK6AJstknNJhsFg9M8YuRD"
    PORT = "16887"
    redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)
    if redis1.exists(msg):
        X = int(redis1.get(msg).decode())
        count = X + 1
    else:
        count = 1
    redis1.set(msg, count)
    return count

# Handler function for Sticker Message
def handle_StickerMessage(event):
    # For the inline sticker
    if int(event.message.package_id) >= 2000000:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("Sorry!!!test, your sticker is not in available sticker list.")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(
                package_id=event.message.package_id,
                sticker_id=event.message.sticker_id)
        )

# Handler function for Image Message
def handle_ImageMessage(event):
    # Resources/Detect Image Message.jpg
    line_bot_api.reply_message(
	    event.reply_token,
        ImageSendMessage(
            original_content_url='https://comp7940cloudcomputing.oss-cn-beijing.aliyuncs.com/Detect%20Image%20Message.jpg',
            preview_image_url='https://comp7940cloudcomputing.oss-cn-beijing.aliyuncs.com/Detect%20Image%20Message.jpg'
        )
    )

# Handler function for Video Message
def handle_VideoMessage(event):
    # Resources/Detect Video Message.mp4
    line_bot_api.reply_message(
	    event.reply_token,
        VideoSendMessage(
            original_content_url='https://comp7940cloudcomputing.oss-cn-beijing.aliyuncs.com/Detect%20Video%20Message.mp4',
            preview_image_url='https://comp7940cloudcomputing.oss-cn-beijing.aliyuncs.com/Detect%20Video%20Message.jpg'
        )
    )

# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Nice file!")
    )

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)
