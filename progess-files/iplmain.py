import time
import boto3
import logging
import os

from winnerintent import winnerintent

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# athena constant
DATABASE = 'ipldataset'
TABLE = 'inputiplbucket'

# S3 constant
S3_OUTPUT = 's3://outputiplbucket/'
S3_BUCKET = 'outputiplbucket'

# query constant
COLUMN = 'team1'

def dateRev(inp):
    year,day,month=inp.split("-")
    newDate = day+"/"+month+"/"+year[2:]
    return newDate

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }

def close(session_attributes, fulfillment_state, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    
    
    
def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }




def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }
    

def validate_ipl_data(team_one, team_two, date):

    if date is not None:
        if not isvalid_date(date):
            return build_validation_result(False, 'Date', 'I did not understand that, whats the date of the match')
        elif datetime.datetime.strptime(date, '%Y-%m-%d').date() <= datetime.date.today():
            return build_validation_result(False, 'Date', '')


    return build_validation_result(True, None, None)
    

def iplwinner(intent_request):


    slots = {}
    slots["team_one"] = get_slots(intent_request)["team_one"]
    slots["team_two"] = get_slots(intent_request)["team_two"]
    slots["date"] = dateRev(get_slots(intent_request)["match_date"])
    slots["source"] = intent_request['invocationSource']
    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)
        
        
        validation_result = validate_ipl_data(team_one,team_two,date)
        validation_result['isValid'] = True
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                                intent_request['currentIntent']['name'],
                                slots,
                                validation_result['violatedSlot'],
                                validation_result['message'])


        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}


        return delegate(output_session_attributes, get_slots(intent_request))

    # In a real bot, this would likely involve a call to a backend service.
    winnerResult = winnerintent(DATABASE, TABLE, S3_OUTPUT,slots)
    if (winnerResult=="unknown"):
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Sorry. I cannot find a record. Please check your question.'})
    else:
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Winner is  {} '.format(winnerResult)})


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'iplwinner':
        return iplwinner(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    os.environ['TZ'] = 'Asia/Kolkata'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    
    responseObject = dispatch(event)
    return responseObject
