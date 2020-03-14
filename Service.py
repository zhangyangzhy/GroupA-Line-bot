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
    FollowEvent, PostbackEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, FileMessage, StickerMessage, StickerSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, LocationMessage, AudioMessage
)
from linebot.utils import PY3
from ZHY import ProcessMessage
import json

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
        if isinstance(event,FollowEvent):
            handle_FollowEvent(event)
        if isinstance(event,PostbackEvent):
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

# Handler function for Follow Event
def handle_FollowEvent(event):
    button_template_message = ButtonsTemplate(
        thumbnail_image_url="https://obs.line-scdn.net/0h_TFUioZ5AHt7LCh0KO1_LFpxCxlITh5wWUpIGVwkXE1RHEBDExhPHg0sWhwBT0AuT0gbHjAsVh5XFUQrQA9OTg4pV09fGw/f256x256",
        title='Module List',
        text='Welcome to follow, click one to get the module tutorial:',
        image_size="contain",
        actions=[
            PostbackAction(
                label='Publish & Search', data='#Module 1 Tutorial'
            ),
            PostbackAction(
                label='News Summaries', data='#Module 2 Tutorial'
            ),
            PostbackAction(
                label='Anti-Coronavirus', data='#Module 3 Tutorial'
            ),
        ]
    )
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text="Follow Event",
            template=button_template_message
        )
    )

# Handler function for Postback Event
def handle_PostbackEvent(event):
    if event.postback.data == "#Module 1 Tutorial":
        msg = '''Module 1 Tutorial:

1. Reply '#My Information' to find the historical store information that you have published;

2. Reply '#Publish Information' to publish the information;

3. Reply '#Search Information' to query the records within 10KM of your current location;

4. Reply '#Delete Information-Record ID' to delete the specific record you have published permanently;

5. Reply '#Modify Information-Record ID' to modify the attribute value;

6. Reply '#Comment-Record ID' to comment on store information that is not published by yourself;

7. Reply '#Rate-Record ID' to rate the credibility of store information;

8. Reply '#Exit' to terminate the current procedure.'''
    elif event.postback.data == "#Module 2 Tutorial":
        msg = '''Module 2 Tutorial:
TO DO...
Written by WU Peicong'''
    elif event.postback.data == "#Module 3 Tutorial":
        msg = '''Module 3 Tutorial:
TO DO...
Written by LI Jinhui'''
    else:
        msg = "Error"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
    )

# Handler function for Text Message
def handle_TextMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(ProcessMessage(event.source.user_id, event.message.text).public("TextMessage"))
    )

# Handler function for Location Message
def handle_LocationMessage(event):
    dic = {"latlng": str(event.message.latitude) + "," + str(event.message.longitude),"address":event.message.address}
    text = json.dumps(dic)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(ProcessMessage(event.source.user_id, text).public("LocationMessage"))
    )

# Handler function for Sticker Message
def handle_StickerMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(ProcessMessage(event.source.user_id, event.message.id).public("StickerMessage"))
    )

# Handler function for Image Message
def handle_ImageMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(ProcessMessage(event.source.user_id, event.message.id).public("ImageMessage"))
    )

# Handler function for Video Message
def handle_VideoMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(ProcessMessage(event.source.user_id, event.message.id).public("VideoMessage"))
    )

# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(ProcessMessage(event.source.user_id, event.message.id).public("FileMessage"))
    )

# Handler function for Audio Message
def handle_AudioMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(ProcessMessage(event.source.user_id, event.message.id).public("AudioMessage"))
    )

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)
