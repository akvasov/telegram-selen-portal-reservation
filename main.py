"""
This program listens for the gym booking commands coming in a Telegram chat window, parses them and calls
'gym_resv' module to initiate the reservation process over the gym's Webportal.
Reservation request should be sent 2 days in advance. Since reservation on the same day is prohibited by the gym policy,
the app will wait till midnight next day to initiate reservation for the day after.
All user defined variables are stored in .env file. You'll need to know your telegram phone and password to
interact with Telegram API.

Telegram chat message format:
'Reserve <facility> <num_ppl> <time_arg_1> <time_arg_2>'

:param facility: new or old facility (each has different web address)
:param num_ppl: 1 or 2 | number of people reserving a gym from my name
:param time_arg_1: most preferred 1 hour time frame to reserve a gym
:param time_arg_2: least preferred 1 hour time frame to reserve a gym

Examples:
'Reserve new 2 4:5pm 5:6pm'
'Reserve old 1 10:11am 2:3pm'
"""

import pause
import datetime
import random
import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

from gym_res_selenium import gym_resv

# Loading all env variables from .env local file
load_dotenv()

# Defining Telegram Client using API id and hash data provided by Telegram for my user
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
client = TelegramClient('session_name', api_id, api_hash)


@client.on(events.NewMessage(pattern='Reserve.+', chats=int(os.environ.get('PRIVATE_GROUP_BOT_API_ID'))))
async def handler(event):
    """
    Waiting for new message with format 'Reserve .*' to arrive in Telegram chat created as part of chat BOT API.
    Extracting arguments from this message.
    Pausing till couple of minutes after midnight next day to initiate reservation process (call module 'gym_resv')
    Sending a result in the chat based on the reservation status
    """
    user_message = event.message.to_dict()['message']
    # Extracting arguments from the message.
    facility, num_ppl, time_arg_1, time_arg_2 = user_message.split(' ')[1:]
    # Pause till couple of minutes after midnight next day
    tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
    tomorrow_year, tomorrow_month, tomorrow_day = tomorrow.split('-')[:]
    pause.until(datetime.datetime(int(tomorrow_year), int(tomorrow_month),
                                  int(tomorrow_day), 00, random.randint(2, 9), 00, 00))
    try:   
        result = gym_resv(facility, num_ppl, time_arg_1, time_arg_2)  # Initiate reservation process
        if result:
            await event.respond('#####!!Reserved#####')
        else:
            await event.respond('#####Reservation Failure! - No avaliable time'
                                          ' -or- wrong input arguments#####')
    except:
            await event.respond('#####Reservation Failure! - Script Failure#####')

client.start()
client.run_until_disconnected()





