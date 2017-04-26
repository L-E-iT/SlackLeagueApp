import random
from cassiopeia import riotapi
from slacker import Slacker
from flask import Flask, request, Response
import os

app = Flask(__name__)

SLACK_WEBHOOK_SECRET = os.environ.get("SlackWebSecret")

# Set some variables that we store in our .bashrc file on the server
slack = Slacker(os.environ.get("SlackerKey"))
riotapi.set_region("NA")
riotapi.set_api_key(os.environ.get("RiotApiKey"))

# Setting a send message function to keep the app more modular
def send_message(channel_name, message):
    slack.chat.post_message(channel_name, message)

# Command to get the rank of a champion.
# Sends back the following:
# Summoner name
# Rank
# LP
@app.route('/rank', methods=['POST'])
def rank():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        text = request.form.get('text')
        summoner = riotapi.get_summoner_by_name(text)
        rank = riotapi.get_league_entries_by_summoner(summoner)
        rankInfo = [rank[0].tier, rank[0].entries[0].division, rank[0].entries[0].league_points]
        message = str(text) + " is currently " + str(rankInfo[0])[5:].capitalize() + " " + str(rankInfo[1])[9:].capitalize() + " with " + str(rankInfo[2]) + " lp."
        send_message(channel,message)
    return Response(),200

# Route for handling accidental Web HTTP requests to the flask server
@app.route('/', methods=['GET'])
def test():
    return Response('Hm... you should go here instead: www.branwidth.com')
    print("it worked")

# Setting SSL values and running application
if __name__ == "__main__":
    context = (os.environ.get("SSLCert"),os.environ.get("SSLPrivKey"))
    app.run(debug=True, host='0.0.0.0',ssl_context=context)
