# Import Pytest module
import pytest

# Sample input stream
input = [{u'source_team': u'TT5FBM2GY', u'channel': u'DT8SL4PL1', u'event_ts': u'1580874944.000500', u'suppress_notification': False, u'ts': u'1580874944.000500', u'text': u'<@UT7HE84AX> test05', u'user': u'UT67Y21B2', u'team': u'TT5FBM2GY', u'type': u'message', u'user_team': u'TT5FBM2GY'}]

# Test for slack communication
@pytest.fixture
def slackCommunication():
    from slack_bot import slackCommunication
    return slackCommunication()

# Test for the main function
@pytest.fixture
def mainFunc():
    from slack_bot import mainFunc
    return mainFunc()

# Test for slack connection
#@pytest.mark.skip(reason='Tested')
def test_slackConnect(slackCommunication):
    assert slackCommunication.slackConnect() == True

# Testing the channel, input and message with the input stream
# Echo sample "test05" if succesful
def test_parseSlackInput(slackCommunication):
    assert slackCommunication.parseSlackInput(input, "UT7HE84AX") == ["UT67Y21B2","test05","DT8SL4PL1"]

# Test for Bot ID and verifying that it is correct
def test_getBotID(slackCommunication):
    assert slackCommunication.getBotID("echo_bot") == "UT7HE84AX"

# Test to write back to slack using the channel number
def test_writeToSlack(slackCommunication):
    assert slackCommunication.writeToSlack("DT8SL4PL1", "Test write to slack")["ok"] == True

# Test for reading of input stream
#@pytest.mark.skip(reason='Not Completed')
def test_slackReadRTM(slackCommunication):
    slackCommunication.slackConnect()
    print slackCommunication.slackReadRTM()

# Test for writing the message back to slack
def test_decideToAction_Message(mainFunc):
    input = ["UT67Y21B2","test05","DT8SL4PL1"]
    assert mainFunc.decideToAction(input)

# Test for ignoring empty input stream
def test_decideToAction_None(mainFunc):
    input = [None, None, None]
    assert mainFunc.decideToAction(input)
