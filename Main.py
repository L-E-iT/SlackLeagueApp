import random
from cassiopeia import riotapi
from slacker import Slacker
from flask import Flask, request, Response
import os

ASSETS_DIR = os.path.dirname(os.path.abspath())

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = "ULs9LTwlPrVTUP8CkTZYPuH1"

slack = Slacker("xoxb-171642061520-h7f1IZCj3b69JxL7JagsjMfN")
riotapi.set_region("NA")
riotapi.set_api_key("RGAPI-84f4a9e5-b6fd-493e-9786-0ccfde1147d4")

summoner = riotapi.get_summoner_by_name("TheBranHammer")
# print("{name} is a level {level} summoner on the NA server.".format(name=summoner.name, level=summoner.level))

# Send a message to #general channel
# slack.chat.post_message('#league', 'Hello summoners!')

def send_message(channel_name, message):
    slack.chat.post_message(channel_name, message)

@app.route('/postgame', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + "says: " + text
        print(inbound_message)
    return Response(), 200

@app.route('/', methods=['GET'])
def test():
    return Response('It works!')
    print("it worked")

if __name__ == "__main__":
    context = ()
    app.run(debug=True, host='0.0.0.0')
