# Import packages from slackclient and OpenWeatherMap
from slackclient import SlackClient
import time
import pyowm

# Slack Communication Class
class slackCommunication(object):

    # Init function
    def __init__ (self):
        # Slack Client Token
        self.slack_client = SlackClient("xoxb-923521716576-926514946866-tCYVYitveEPU20Cjbv9GAf2T")
        # Open Weather Map Token
        self.owm = pyowm.OWM('da2b0d4b03873b46ec69f3f5fd1933d6')
        # Slackbot name
        self.appName = "weather_bot"

    # Slack Connection Function using rtm_connect()    
    def slackConnect(self):
        return self.slack_client.rtm_connect()

    # Read the user slack input
    def slackReadRTM(self):
        return self.slack_client.rtm_read()

    # Parse the received Slack Input from the user
    def parseSlackInput(self,input, botID):
        botATID = "<@"+botID+">"
        if input and len(input) > 0:
            input = input[0]
            # Extract user, message and channel information from the input stream
            if 'text' in input and botATID in input['text']:
                user = input['user']
                message = input['text'].split(botATID)[1].strip(' ')
                channel = input['channel']
                return [str(user), str(message), str(channel)]
            else:
                return [None, None, None]

    # Get the BotID using the API call and extract only the registered members
    def getBotID(self,botusername):
        api_call = self.slack_client.api_call("users.list")
        users = api_call['members']
        for user in users:
            if 'name' in user and botusername in user.get('name') and not user.get('deleted'):
                return user.get('id')

    # Write back to the slack client using channel, text and POST function
    def writeToSlack(self,channel,message):
        return self.slack_client.api_call("chat.postMessage", channel = channel , text = message, as_user = True)

# Main Function
class mainFunc(slackCommunication):
    # Main Function and get BotID
    def __init__(self):
        super(mainFunc, self).__init__()
        BOTID = self.getBotID(self.appName)

    # Send the user input from slack to OpenWeather Map API for weather information    
    def decideToAction(self, input):
        if input:
            user, message, channel = input
            msg = str(message)
            # Send the message to Open Weather Map
            observation = self.owm.weather_at_place(msg)
            weather = observation.get_weather()
            temperature = weather.get_temperature('celsius')['temp']
            str1 = 'The temperature is '
            str2 = ' degrees celsius and '
            # Convert message to string format
            temperature = str(temperature)
            status = weather.get_detailed_status()
            msg2 = str1 + temperature + str2 + status
            # Write the message from Open Weather Map back to Slack
            return self.writeToSlack(channel,msg2)

    # Run Function    
    def run(self):
        # Run the slack connect function
        self.slackConnect()
        # Get the Bot ID for the slack communication
        BOTID = self.getBotID(self.appName)
        while True:
            # Send the parsed input to Open Weather Map API and write the message back to slack
            self.decideToAction(self.parseSlackInput(self.slackReadRTM(),BOTID))
            time.sleep(1)

# Run Main function 
if __name__ == "__main__":
    instance = mainFunc()
    instance.run()
