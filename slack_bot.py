# Import slackclient module
from slackclient import SlackClient
import time

# Slack Communication Function
class slackCommunication(object):

    # Init function
    def __init__ (self):
        # Connect to slackclient using the token
        self.slack_client = SlackClient("xoxb-923521716576-925592276371-oKFyX2k3P5JKuh2wrjbJy4IY")
        # Slackbot name
        self.appName = "echo_bot"

    # Slack Connect message using rtm_connect() function    
    def slackConnect(self):
        return self.slack_client.rtm_connect()

    # Read the slack input stream using rtm_read() function
    def slackReadRTM(self):
        return self.slack_client.rtm_read()

    # Parse the received input stream using the Bot ID
    def parseSlackInput(self,input, botID):
        botATID = "<@"+botID+">"
        if input and len(input) > 0:
            input = input[0]
            # Extract user, message and channel from the input stream
            if 'text' in input and botATID in input['text']:
                user = input['user']
                message = input['text'].split(botATID)[1].strip(' ')
                channel = input['channel']
                return [str(user), str(message), str(channel)]
            else:
                return [None, None, None]
    
    # Get the Bot ID using the Slack API call
    def getBotID(self,botusername):
        api_call = self.slack_client.api_call("users.list")
        # Id the members exist, then get the Bot ID for that user
        users = api_call['members']
        for user in users:
            if 'name' in user and botusername in user.get('name') and not user.get('deleted'):
                return user.get('id')

    # Write the input message back to slack (echo message)
    def writeToSlack(self,channel,message):
        return self.slack_client.api_call("chat.postMessage", channel = channel , text = message, as_user = True)

# Main Function
class mainFunc(slackCommunication):
    def __init__(self):
        super(mainFunc, self).__init__()
        # Get Bot ID for the echo_bot 
        BOTID = self.getBotID(self.appName)

    # Function to write mesage to slack using channel and message parameters
    def decideToAction(self, input):
        if input:
            user, message, channel = input
            return self.writeToSlack(channel,message)

    # Run Function 
    def run(self):
        # Connect to slack
        self.slackConnect()
        # Get Bot ID
        BOTID = self.getBotID(self.appName)
        while True:
            # Read input stream, parse the message and write the message back to slack
            self.decideToAction(self.parseSlackInput(self.slackReadRTM(),BOTID))
            time.sleep(1)

if __name__ == "__main__":
    instance = mainFunc()
    instance.run()
            
