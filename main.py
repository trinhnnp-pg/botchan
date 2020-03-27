from flask import Flask, request, Response
import os
import requests
import json
import random
from classes import Subject, Observer

app = Flask(__name__) 
  
@app.route("/")
def route():
    print(os.environ)
    return "<h1>Welcome to Chatbot</h1>"

# env_variables
# token to verify that this bot is legit
# verify_token = os.environ.get('VERIFICATION_TOKEN', '')
VERIFY_TOKEN = 'testtest'
# token to send messages through facebook messenger
# access_token = os.environ.get('PAGE_ACCESS_TOKEN', '')
PAGE_ACCESS_TOKEN = 'EAAgq7sbY3nwBAKCROoVSDwr2Hq2r84ojEKZBymZBdXBhtcZCLHkZBaKTxYtr4sZCizt6zEpJu1ODA0yIqTEHf2BylZBHSnlngLkx73jatn6R4mZAG6xuj53p7ZAw2N76J6vzwsDK6QGLiLt7cZBBEF3AwRydF39uSekYn5pwf5mKuOgZDZD'
SUBSCRIBE_TXT = 'follow'
DESUBSCRIBE_TXT = 'unfollow'

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@app.route('/webhook', methods=['POST'])
def webhook_action():
    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        user_message = entry['messaging'][0].get('message', '')
        if user_message:
            user_message = user_message.get('text', '')
        user_id = entry['messaging'][0]['sender']['id']
        response = {
            'recipient': {'id': user_id},
            'message': {}
        }
        response['message']['text'] = handle_request_message(user_id, user_message)
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + PAGE_ACCESS_TOKEN, json=response)
    print('#'*20)
    return Response(response="EVENT RECEIVED",status=200)


from string import Template
def autopush_action(observer, value):
    user_id = observer.observer_id
    response_tpl = Template('Chú ý bạn êi, Việt Nam mới cập nhật số ca nhiễm Covid-19. Hiện tại là: $value ca')
    response = {
        'recipient': {'id': user_id},
        'message': {}
    }
    response['message']['text'] = response_tpl.substitute(value=value)
    r = requests.post(
        'https://graph.facebook.com/v2.6/me/messages/?access_token=' + PAGE_ACCESS_TOKEN, json=response)
    return Response(response="EVENT RECEIVED",status=200)

SUBJECT = Subject(autopush_action)

# new_observer = Observer('3227701563907768', autopush_action)
# SUBJECT.attach(new_observer)
# new_observer = Observer('3714350231970997', autopush_action)
# SUBJECT.attach(new_observer)

def handle_request_message(user_id, user_message):
    # DO SOMETHING with the user_message ... ¯\_(ツ)_/¯
    if user_message:
        response_txt = 'Huhu bạn nói gì bot chan ko hiểu'
    else:
        response_txt = ''
    if user_message.lower() == SUBSCRIBE_TXT:
        response_txt = "Oke! Bot chan sẽ tích cực hóng hớt và cập nhật cho bạn"
        new_observer = Observer(user_id)
        SUBJECT.attach(new_observer)
    if user_message.lower() == DESUBSCRIBE_TXT:
        response_txt = "Ok... Níu kéo cũng ko hạnh phúc"
        new_observer = Observer(user_id)
        SUBJECT.detach(new_observer)
    return response_txt


# from time import time, sleep
# starttime = time()
# SCHEDULE_TIME = 60.0
# INNIT = 0
# while True:
#     INNIT += SCHEDULE_TIME
#     print(INNIT)
#     SUBJECT.change(INNIT)
#     sleep(SCHEDULE_TIME - ((time() - starttime) % SCHEDULE_TIME))

import schedule

INNIT = 0
SCHEDULE_TIME = 10
def geeks():
    # global INNIT
    # INNIT += SCHEDULE_TIME
    # print(INNIT)
    # SUBJECT.change(INNIT)
    print("Shaurya says Geeksforgeeks")

schedule.every(10).seconds.do(geeks) 


def handle_message(user_id, user_message):
    # DO SOMETHING with the user_message ... ¯\_(ツ)_/¯
    response_txt = ''
    if user_message:
        response_txt = "Hello "+user_id+" ! You just sent me : " + user_message
    return response_txt

@app.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."
