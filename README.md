# telegram-selen-portal-reservation
## Description
This program listens for the gym booking commands coming in a Telegram chat window, parses them and calls
Selenium based custom module to initiate the reservation process over the gym's Webportal.
Reservation request should be sent 2 days in advance. Since reservation on the same day is prohibited by the gym policy,
the app will wait till midnight next day to initiate reservation for the day after.
All user defined variables are stored in .env file. You'll need to know your telegram phone and password to
interact with Telegram API.

Telegram chat message format:
~~~
'Reserve <facility> <num_ppl> <time_arg_1> <time_arg_2>'

  
:param facility: new or old facility (each has different web address)
:param num_ppl: 1 or 2 | number of people reserving a gym from my name
:param time_arg_1: most preferred 1 hour time frame to reserve a gym
:param time_arg_2: least preferred 1 hour time frame to reserve a gym
~~~
Examples:
~~~
'Reserve new 2 4:5pm 5:6pm'
'Reserve old 1 10:11am 2:3pm'
~~~

## Installation
See 'requirements.txt'

CentOS base packages installation and setup:
~~~
yum groupinstall “Development Tools”
yum install pip3.6
~~~
#Install geckodriver for Selenium module to interact with Mozilla browser
~~~
wget -o https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
tar -xvf geckodriver-v0.30.0-linux64.tar.gz
sudo cp geckodriver /usr/local/bin
sudo chmod +x /usr/local/bin/geckodriver
export PATH=$PATH:/usr/local/bin/geckodriver
~~~

Python modules
~~~
pip3 install selenium
pip3 install telethon
pip3 install python-dotenv
~~~

## Implementation
Works with python3.6 or newer.
Application spins up and stays active until keyboard interrupted.
~~~
]$ python3.6 main.py 
~~~

### .env file variables
~~~
'NEW_GYM_PAGE'  # New gym reservation Webpage
'OLD_GYM_PAGE'  # Old gym reservation Webpage
'PERSON_1'  # First person name to reserve a gym
'PERSON_2'  # Second person name to reserve a gym
'SIGNIN_EMAIL'  # Reservation Webpage signing email address
'SIGNIN_PASSWD'  # Reservation Webpage signing email address 
'API_ID'  # Telegram APP API ID
'API_HASH'  # Telegram APP hash ID
'PRIVATE_GROUP_BOT_API_ID'  # Telegram BOT API ID
~~~
