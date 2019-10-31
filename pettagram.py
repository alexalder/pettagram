import json
import urllib.request, urllib.parse, urllib.error
import requests
import traceback

from flask import Flask, request, make_response

base_url: str


# Returns the sent message as JSON
def send(chat_id, msg=None, photo_id=None, reply=None, keyboard=json.dumps({'inline_keyboard': [[]]}), parse_mode=None, disable_preview='true'):
    try:
        if photo_id:
            resp = urllib.request.urlopen(base_url + 'sendPhoto', urllib.parse.urlencode({
                'chat_id': str(chat_id),
                'photo': photo_id,
                'caption': msg.encode('utf-8'),
                'parse_mode': 'Markdown',
                'reply_to_message_id': str(reply),
                'reply_markup': keyboard,
            }).encode('utf-8')).read()
        elif msg:
            resp = urllib.request.urlopen(base_url + 'sendMessage', urllib.parse.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'parse_mode': parse_mode,
                    'disable_web_page_preview': disable_preview,
                    'reply_to_message_id': reply,
                    'reply_markup': keyboard,
                }).encode('utf-8')).read()
        else:
            print("No message to send")
            resp = make_response("No message to send")
            return resp
        print('Sent message:')
        print(resp)
    except urllib.error.HTTPError as e:
        print("Error in send: " + e.read().decode())
        resp = make_response("Error in send")
    except Exception:
        print("Error in send: " + traceback.format_exc())
        resp = make_response("Error in send")
    return resp


def send_file(chat_id, photo=None, video=None, reply=None, keyboard=json.dumps({'inline_keyboard': [[]]})):
    try:
        if photo:
            url = base_url + 'sendPhoto'
            files = {'photo': open(photo, 'rb')}
        elif video:
            url = base_url + 'sendVideo'
            files = {'video': open(video, 'rb')}
        data = {'chat_id': chat_id}
        resp = requests.post(url, files=files, data=data).json()
        print('Sent file:')
        print(resp)
    except Exception:
        print("Error in send_file: " + traceback.format_exc())
        resp = make_response('Error in send_file')
    return resp


def edit_message(chat_id, message_id, text):
    try:
        resp = urllib.request.urlopen(base_url + 'editMessageText', urllib.parse.urlencode({
                'chat_id': str(chat_id),
                'message_id': int(message_id),
                'text': text.encode('utf-8'),
                'parse_mode': 'Markdown',
                'disable_web_page_preview': 'true',
            }).encode('utf-8')).read()
        print(resp)
    except Exception:
        resp = make_response('Error in edit')
    return resp


def delete_message(chat_id, message_id):
    try:
        resp = urllib.request.urlopen(base_url + 'deleteMessage', urllib.parse.urlencode({
                'chat_id': str(chat_id),
                'message_id': int(message_id),
            }).encode('utf-8')).read()
        print(resp)
    except Exception:
        resp = make_response('Error in delete')
    finally:
        return resp


def edit_markup(chat_id, message_id, keyboard):
    try:
        resp = urllib.request.urlopen(base_url + 'editMessageReplyMarkup', urllib.parse.urlencode({
                'chat_id': str(chat_id),
                'message_id': int(message_id),
                'reply_markup': keyboard,
            }).encode('utf-8')).read()
        print(resp)
    except Exception:
        resp = make_response('Error in edit')
    return resp


def edit_caption(chat_id, message_id, caption, keyboard=json.dumps({'inline_keyboard': [[]]})):
    try:
        resp = urllib.request.urlopen(base_url + 'editMessageCaption', urllib.parse.urlencode({
                'chat_id': str(chat_id),
                'message_id': int(message_id),
                'caption': caption,
                'parse_mode': 'Markdown',
                'reply_markup': keyboard,
            }).encode('utf-8')).read()
        print(resp)
    except Exception:
        resp = make_response('Error in edit')
    return resp

    
def answer_callback(query_id):
    try:
        resp = urllib.request.urlopen(base_url + 'answerCallbackQuery', urllib.parse.urlencode({
                'callback_query_id': query_id,
            }).encode('utf-8')).read()
    except Exception:
        resp = make_response('Error in callbackanswer')
    finally:
        return resp


def pin(message_id, chat_id, notification=True):
    try:
        resp = urllib.request.urlopen(base_url + 'pinChatMessage', urllib.parse.urlencode({
            'chat_id': str(chat_id),
            'message_id': int(message_id),
            'disable_notification': not notification, }).encode('utf-8')).read()
    except Exception:
        resp = make_response('Error in pin')
    finally:
        return resp


def get_file(file_id):
    query = urllib.request.urlopen(base_url + 'getFile', urllib.parse.urlencode({
        'file_id': str(file_id),
        }).encode("utf-8")).read()
    answer = json.loads(query).get("result")
    return answer.get('file_path')
