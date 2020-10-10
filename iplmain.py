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
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    
    

def iplwinner(intent_request):
    """
    Performs dialog management and fulfillment for ordering flowers.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    slots = {}
    slots["team_one"] = get_slots(intent_request)["team_one"]
    slots["team_two"] = get_slots(intent_request)["team_two"]
    slots["date"] = get_slots(intent_request)["match_date"]
    slots["source"] = intent_request['invocationSource']
    
    # if source == 'DialogCodeHook':
    #     # Perform basic validation on the supplied input slots.
    #     # Use the elicitSlot dialog action to re-prompt for the first violation detected.
    #     slots = get_slots(intent_request)

    #     # validation_result = validate_order_flowers(flower_type, date, pickup_time)
    #     # validation_result['isValid'] = True
    #     if not validation_result['isValid']:
    #         slots[validation_result['violatedSlot']] = None
    #         return elicit_slot(intent_request['sessionAttributes'],
    #                            intent_request['currentIntent']['name'],
    #                            slots,
    #                            validation_result['violatedSlot'],
    #                            validation_result['message'])

    #     # Pass the price of the flowers back through session attributes to be used in various prompts defined
    #     # on the bot model.
    #     output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    #     if flower_type is not None:
    #         output_session_attributes['Price'] = len(flower_type) * 5  # Elegant pricing model

    #     return delegate(output_session_attributes, get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    winnerResult = winnerintent(DATABASE, TABLE, S3_OUTPUT,slots)
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
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
