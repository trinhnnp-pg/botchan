from flask import Flask, request, Response
import os
import requests
import json
import random

app = Flask(__name__) 
  
@app.route("/")
def route():
    print(os.environ)
    return "<h1>Welcome to Chatbot</h1>"

# env_variables
# token to verify that this bot is legit
# verify_token = os.environ.get('VERIFICATION_TOKEN', '')
verify_token = 'testtest'
# token to send messages through facebook messenger
# access_token = os.environ.get('PAGE_ACCESS_TOKEN', '')
access_token = 'EAAgq7sbY3nwBAKCROoVSDwr2Hq2r84ojEKZBymZBdXBhtcZCLHkZBaKTxYtr4sZCizt6zEpJu1ODA0yIqTEHf2BylZBHSnlngLkx73jatn6R4mZAG6xuj53p7ZAw2N76J6vzwsDK6QGLiLt7cZBBEF3AwRydF39uSekYn5pwf5mKuOgZDZD'

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@app.route('/webhook', methods=['POST'])
def webhook_action():
    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        user_message = entry['messaging'][0].get('message', [])
        if user_message:
            user_message = user_message.get('text', '')
        user_id = entry['messaging'][0]['sender']['id']
        response = {
            'recipient': {'id': user_id},
            'message': {}
        }
        response['message']['text'] = handle_message(user_id, user_message)
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)
    print('#'*20)
    return Response(response="EVENT RECEIVED",status=200)


@app.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = json.loads(request.data.decode('utf-8'))
    user_message = data['entry'][0]['messaging'][0].get('message', [])
    if user_message:
        user_message = user_message.get('text', '')
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    response = {
        'recipient': {'id': user_id},
        'message': {'text': handle_message(user_id, user_message)}
    }
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

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
