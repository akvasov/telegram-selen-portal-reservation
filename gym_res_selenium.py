"""
This program helps to automate my apartment building gym reservation process leveraging Selenium module methods
to fill out Webforms.
All user defined variables are stored in .env file.
"""

import time
import os
import sys
import datetime
import argparse

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import Select


def midday_check(time_arg):
	"""
	Function analyses user defined 1 hour time frame system argument to access a gym and parses it to the time format
	suitable for gym reservation Website.
	For example:
	- '3:4pm' argument will be parsed to '3:00PM-4:00PM'
	- '11:12pm' argument will be parsed to '11:00AM-12:00PM'

	:param time_arg: user defined time 1h frame system argument to access a gym (x:y[am|pm])
	:return: time format suitable for gym reservation Website (X[AM|PM]-Y[AM|PM])
	"""
	if time_arg.split(':')[0] == '11':
		return time_arg.split(':')[0] + ":00" + ' ' + 'AM' + " - " + time_arg.split(':')[1][:-2] \
			   + ':00' + ' ' + time_arg[-2:].upper()
	else:
		return time_arg.split(':')[0] + ":00" + ' ' + time_arg[-2:].upper() + " - " \
			   + time_arg.split(':')[1][:-2] + ':00' + ' ' + time_arg[-2:].upper()


def page_is_loaded(driver):
	"""Selenium required method to load the Webpage"""
	return driver.find_element_by_tag_name("body") != None


def gym_resv(facility, num_ppl, time_arg_1, time_arg_2):
	"""
	This function receives system arguments to login on the fitness center webpage using my credentials
	and make a gym reservation based on two defined 1hour time frames for next day (most and least preferred time frames
	I'd like to reserve a gym).
	Per gym rules reservations can be made next day only. Reservations are only 1hour duration.
	New gym can be reserved by 1 or 2 people, old - just 1 person.

	:param facility: new or old facility (each has different web address)
	:param num_ppl: 1 or 2 | number of people reserving a gym from my name
	:param time_arg_1: most preferred 1 hour time frame to reserve a gym. Example: 4:5pm
	:param time_arg_2: least preferred 1 hour time frame to reserve a gym. Example: 2:3pm
	:return: True if reservation is successful, None if not
	"""
	# Code block to analyse system arguments and assign them to the variables
	if facility == 'new':
		gym_url = os.environ.get('NEW_GYM_PAGE')
	elif facility == 'old':
		gym_url = os.environ.get('OLD_GYM_PAGE')
	else:
		print("You must pick new or old gym for the fist argument")
		return None

	if (num_ppl == '2') and (facility == 'new'):
		resv_list = [2, os.environ.get('PERSON_1'), os.environ.get('PERSON_2')]
	elif num_ppl == '1':
		resv_list = [1, os.environ.get('PERSON_1')]
	else:
		print("You must pick 1 or 2! Note: old center fits only 1 visitor!")
		return None

	my_time_1 = midday_check(time_arg_1)  # my preferred time to reserved
	my_time_2 = midday_check(time_arg_2)  # my less preferred time to reserved

	# Code block to initialize Selenium webdriver
	avail_pointer = None  # local variable to help with timeframes assignment
	driver = webdriver.Firefox()
	driver.get(gym_url)
	wait = ui.WebDriverWait(driver,10)
	wait.until(page_is_loaded)

	# Code block to Login on the gym's reservation Webpage
	user = driver.find_element_by_name("UserName")
	password = driver.find_element_by_name("password")
	user.clear()
	user.send_keys(os.environ.get('SIGNIN_EMAIL'))
	password.clear()
	password.send_keys(os.environ.get('SIGNIN_PASSWD'))
	driver.find_element_by_xpath('//button[@class="submit"]').click()
	time.sleep(6)

	# Main code block to fill up the gym's reservation Webpage form
	# Select a month on a form for tomorrow (reservation is  always supposed to be for next day)
	tomorrow = datetime.date.today() + datetime.timedelta(days=1)
	tomorrow_day = str(tomorrow).split('-')[2].lstrip("0")
	tomorrow_month = tomorrow.strftime("%b")
	#
	driver.find_element_by_id('resv-date').click()
	selected_to_month = Select(driver.find_element_by_xpath("//div/select[@class='ui-datepicker-month']"))
	selected_to_month.select_by_visible_text(tomorrow_month)
	time.sleep(2)
	# Select a date on a form for tomorrow (reservation is  always supposed to be for next day)
	for dates in driver.find_elements_by_xpath(".//*[@id='ui-datepicker-div']/table/tbody/tr/td/a"):
		if dates.is_enabled() and\
			dates.is_displayed() and\
			str(dates.get_attribute("innerText")) == tomorrow_day:
			dates.click()
	time.sleep(2)

	# Select a reservation period from drop-down menu
	time.sleep(2)
	inputs = ui.Select(driver.find_element_by_css_selector('#SelStartTime'))
	for option in inputs.options:
		# It could be some timeframes already reserved by other tenants.
		# So need to check what options are left and if they work for me.
		# We go through the drop-down many one by one in for loop
		# comparing each available timeframe with desired to reserve.
		avail_date = str(option.text)
		if avail_date == "There are no available start times":  # quit the program if everything is booked
			driver.quit()
			time.sleep(4)
			sys.exit(1)

		# It could happen that less desired timeframe will be available in the dropdown list first.
		# So we need to make sure we go further in the dropdown list to check if more priority time is available
		if (my_time_1 > my_time_2) and (my_time_2 in avail_date):
			inputs.select_by_visible_text(option.text)
			avail_pointer = True
			continue      
		if my_time_1 in avail_date: 
			inputs.select_by_visible_text(option.text)
			break
		elif my_time_2 in avail_date:
			inputs.select_by_visible_text(option.text)
			break
	else: 
		if not avail_pointer:  # Quit the program, if all timeframes we want are booked
			driver.quit()
			time.sleep(4)
			sys.exit(1)

	time.sleep(4)

	# Fill out other info like number of people reserving gym and their names
	driver.find_element_by_id('NumberOfPeople').send_keys(Keys.BACKSPACE)
	driver.find_element_by_id('NumberOfPeople').send_keys(resv_list[0])
	time.sleep(2)
	driver.find_element_by_id('ReservationNames').send_keys(resv_list[1])
	time.sleep(3)
	driver.find_element_by_id('reservation-terms').click()  # Reservation-terms checkbox
	time.sleep(4)
	driver.find_element_by_id('submit-new-reservation').click()  # Change to submit-new-reservation
	return True


if __name__ == '__main__':
	"""
	Section defining how to execute this app with system arguments
	"""

	# Help for system variables to use with an app
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''
	
	Usage:
	
	python ./gym.py <old/new> <# of people: 1/2> <pref_time1> <pref_time2>
	
	Usage examples:
	
	python gym.py new 2 4:5pm 5:6pm
	
			'''
		)
	parser.add_argument('strings', metavar='gym_center', type=str, help=
		'''
		Old or New Fitness Center to book
		''')
	parser.add_argument('strings', metavar='num_of_people', type=int, help=
		'''
		 Number of people to visit the center
		''')
	parser.add_argument('strings', metavar='my_time_1', type=str, help=
		'''
		Preffered time to book the center
		''')
	parser.add_argument('strings', metavar='my_time_2', type=str, help=
		'''
		The second preffered time to book the center
		''')
	args = parser.parse_args()

	if len(sys.argv) < 4 or len(sys.argv) > 5:
		print("Incorrect arguments number. Must be 4")
		parser.print_usage()
		sys.exit(1)

	load_dotenv()  # Load system env variables from .env local file
	gym_resv(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])  # Main function call
	
