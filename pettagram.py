import json
import urllib.request, urllib.parse, urllib.error
import requests
import traceback

from flask import make_response


class Bot:
    def __init__(self, base_url):
        self.base_url = base_url

    # Returns the sent message as JSON
    def send(self, chat_id, msg=None, photo_id=None, sticker_id=None, reply=None, keyboard=json.dumps({'inline_keyboard': [[]]}), parse_mode=None, disable_preview='true'):
        try:
            if photo_id:
                resp = requests.get(
                    self.base_url + 'sendPhoto',
                    params={
                        'chat_id': chat_id,
                        'photo': photo_id,
                        'caption': None if msg is None else msg.encode('utf-8'),
                        'parse_mode': parse_mode,
                        'reply_to_message_id': None if reply is None else int(reply),
                        'reply_markup': keyboard,
                    }).content
            elif msg:
                resp = requests.get(
                    self.base_url + 'sendMessage',
                    params={
                        'chat_id': chat_id,
                        'text': msg.encode('utf-8'),
                        'parse_mode': parse_mode,
                        'disable_web_page_preview': disable_preview,
                        'reply_to_message_id': None if reply is None else int(reply),
                        'reply_markup': keyboard,
                    }).content
            elif sticker_id:
                resp = requests.get(
                    self.base_url + 'sendSticker',
                    params={
                        'chat_id': chat_id,
                        'sticker': sticker_id,
                        'reply_to_message_id': None if reply is None else int(reply),
                        'reply_markup': keyboard,
                    }).content
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

    def send_url(self, chat_id, document=None, caption = None):
        try:
            if document:
                resp = requests.get(
                    self.base_url + 'sendDocument',
                    params={
                        'chat_id': chat_id,
                        'document': document,
                        'caption' : caption
                    }).content
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

    def send_file(self, chat_id, photo=None, video=None, document=None, reply=None, keyboard=json.dumps({'inline_keyboard': [[]]})):
        try:
            if photo:
                url = self.base_url + 'sendPhoto'
                files = {'photo': open(photo, 'rb')}
            elif video:
                url = self.base_url + 'sendVideo'
                files = {'video': open(video, 'rb')}
            elif document:
                url = self.base_url + 'sendDocument'
                files = {'document': open(document, 'rb')}
            data = {'chat_id': chat_id, 'reply_to_message_id': reply}
            resp = requests.post(url, files=files, data=data).json()
            print('Sent file:')
            print(resp)
        except Exception:
            print("Error in send_file: " + traceback.format_exc())
            resp = make_response('Error in send_file')
        return resp

    def edit_message(self, chat_id, message_id, text, parse_mode=None):
        try:
            resp = urllib.request.urlopen(self.base_url + 'editMessageText', urllib.parse.urlencode({
                    'chat_id': str(chat_id),
                    'message_id': int(message_id),
                    'text': text.encode('utf-8'),
                    'parse_mode': parse_mode,
                    'disable_web_page_preview': 'true',
                }).encode('utf-8')).read()
            print(resp)
        except urllib.error.HTTPError as e:
            print("Error in update: " + e.read().decode())
            resp = make_response("Error in send")
        except Exception:
            print("Error in update: " + traceback.format_exc())
            resp = make_response("Error in send")
        return resp

    def delete_message(self, chat_id, message_id):
        try:
            resp = urllib.request.urlopen(self.base_url + 'deleteMessage', urllib.parse.urlencode({
                    'chat_id': str(chat_id),
                    'message_id': int(message_id),
                }).encode('utf-8')).read()
            print(resp)
        except Exception:
            resp = make_response('Error in delete')
        finally:
            return resp

    def edit_markup(self, chat_id, message_id, keyboard):
        try:
            resp = urllib.request.urlopen(self.base_url + 'editMessageReplyMarkup', urllib.parse.urlencode({
                    'chat_id': str(chat_id),
                    'message_id': int(message_id),
                    'reply_markup': keyboard,
                }).encode('utf-8')).read()
            print(resp)
        except Exception:
            resp = make_response('Error in edit')
        return resp

    def edit_caption(self, chat_id, message_id, caption, parse_mode=None, keyboard=json.dumps({'inline_keyboard': [[]]})):
        try:
            resp = urllib.request.urlopen(self.base_url + 'editMessageCaption', urllib.parse.urlencode({
                    'chat_id': str(chat_id),
                    'message_id': int(message_id),
                    'caption': caption,
                    'parse_mode': parse_mode,
                    'reply_markup': keyboard,
                }).encode('utf-8')).read()
            print(resp)
        except Exception:
            resp = make_response('Error in edit')
        return resp

    def answer_callback(self, query_id):
        try:
            resp = urllib.request.urlopen(self.base_url + 'answerCallbackQuery', urllib.parse.urlencode({
                    'callback_query_id': query_id,
                }).encode('utf-8')).read()
        except Exception:
            resp = make_response('Error in callbackanswer')
        finally:
            return resp

    def pin(self, message_id, chat_id, notification=True):
        try:
            resp = urllib.request.urlopen(self.base_url + 'pinChatMessage', urllib.parse.urlencode({
                'chat_id': str(chat_id),
                'message_id': int(message_id),
                'disable_notification': not notification, }).encode('utf-8')).read()
        except Exception:
            resp = make_response('Error in pin')
        finally:
            return resp

    def get_file(self, file_id):
        query = urllib.request.urlopen(self.base_url + 'getFile', urllib.parse.urlencode({
            'file_id': str(file_id),
            }).encode("utf-8")).read()
        answer = json.loads(query).get("result")
        return answer.get('file_path')

    def kick(self, chat_id, user_id):
        try:
            resp = urllib.request.urlopen(self.base_url + 'kickChatMember', urllib.parse.urlencode({
                'chat_id': str(chat_id),
                'user_id': int(user_id),
                }).encode('utf-8')).read()
            resp = urllib.request.urlopen(self.base_url + 'unbanChatMember', urllib.parse.urlencode({
                'chat_id': str(chat_id),
                'user_id': int(user_id),
                }).encode('utf-8')).read()
        except Exception:
            resp = make_response('Error in kick')
        finally:
            return resp

    def answer_inline_query(self, query, results):
        try:
            query_id = query["id"]

            resp = requests.get(
                self.base_url + 'answerInlineQuery',
                params={
                    'inline_query_id': query_id,
                    'is_personal': True,
                    'results': results
                }).content
        except urllib.error.HTTPError as e:
            print("Error in send: " + e.read().decode())
            resp = make_response("Error in send")
        except Exception:
            print("Error in send: " + traceback.format_exc())
            resp = make_response("Error in send")

        print('Answer inline query:')
        print(resp)
        return resp
