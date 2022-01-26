import os
import sys
import asyncio
import pause
import datetime
import random

from telethon import TelegramClient, events, sync
from telethon.utils import get_display_name
from telethon.tl.types import InputPeerChat, PeerUser, PeerChat, PeerChannel, User
from main import avalon_resv

api_id = 3721853
api_hash = 'ebf3b7903ad1cf4e1351c830b58b8a9d'

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern='Reserve.+',chats=474116673))
async def handler(event):    
    user_mess = event.message.to_dict()['message']
    facility, num_ppl, time_arg_1, time_arg_2 = user_mess.split(' ')[1:]
    today =  datetime.date.today()
    tomorrow = today + datetime.timedelta(days = 1)
    tomorrow_str = str(tomorrow)
    tomorrow_year, tomorrow_mnth, tomorrow_day = tomorrow_str.split('-')[:]
    pause.until(datetime.datetime(int(tomorrow_year), int(tomorrow_mnth), int(tomorrow_day), 00, random.randint(2,9), 00, 00))
    try:   
             result = avalon_resv(facility, num_ppl, time_arg_1, time_arg_2)
             if result: respond = await event.respond('#####!!Reserved#####')
             else: respond = await event.respond('#####Reservation Failure! - No avaliable time -or- wrong input arguments#####')
    except: respond = await event.respond('#####Reservation Failure! - Script Failure#####') 
 
client.start()
client.run_until_disconnected()





