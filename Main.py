import random
from cassiopeia import riotapi
from slacker import Slacker
from flask import Flask, request, Response
import os

app = Flask(__name__)

# Set some variables that we store in our .bashrc file on the server
SLACK_WEBHOOK_SECRET = os.environ.get("SlackWebSecret")
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
    try:
        if request.form.get('token') == SLACK_WEBHOOK_SECRET:
            # Get channel name and text after command
            channel     = request.form.get('channel_name')
            text        = request.form.get('text')
            # Get summoner information
            summoner    = riotapi.get_summoner_by_name(text)
            # Get ranked information about the summoner
            rank        = riotapi.get_league_entries_by_summoner(summoner)
            rankInfo    = [rank[0].tier, rank[0].entries[0].division, rank[0].entries[0].league_points]
            message     = str(text) + " is currently " + str(rankInfo[0])[5:].capitalize() + " " + str(rankInfo[1])[9:].capitalize() + " with " + str(rankInfo[2]) + " lp."
            send_message(channel,message)
        return Response(),200
    except Exception as e:
        return "I could not find that summoner, maybe they are not ranked yet."

@app.route('/winrate', methods=['POST'])
def winrate():
    try:
        if request.form.get('token') == SLACK_WEBHOOK_SECRET:
            # Code for winrate
            # Get channel name and text after command
            channel     = request.form.get('channel_name')
            text        = request.form.get('text')
            # Get summoner information
            summoner    = riotapi.get_summoner_by_name(text)
            # Get winrates for summoner
            rank        = riotapi.get_league_entries_by_summoner(summoner)
            winrate    = (int(rank[0].entries[0].wins)/(int(rank[0].entries[0].wins) + int(rank[0].entries[0].losses)))
            message     = str(text) + " has a ranked winrate of " + "{0:.0%}".format(winrate)
            print(message)
            send_message(channel,message)
        return Response(),200
    except Exception as e:
        return "I could not find that summoner"


# Route for handling accidental Web HTTP requests to the flask server
@app.route('/', methods=['GET'])
def test():
    return Response('Hm... you should go here instead: www.branwidth.com')
    print("it worked")

# Setting SSL values and running application
if __name__ == "__main__":
    context = ('/etc/letsencrypt/live/branwidth.com/fullchain.pem','/etc/letsencrypt/live/branwidth.com/privkey.pem')
    app.run(debug=True, host='0.0.0.0',ssl_context=context)
