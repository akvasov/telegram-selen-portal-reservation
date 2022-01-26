import time
import sys
import datetime
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def page_is_loaded(driver):
	return driver.find_element_by_tag_name("body") != None

def avalon_resv(facility, num_ppl, time_arg_1, time_arg_2):
	if facility == 'new': 
	     avalon_url = "https://www.avalonaccess.com/Information/Information/AmenityReservation?amenityKey=5db77d39-c8fe-4b1c-b7b6-a14948bb50bc"
	elif facility == 'old': 
	     avalon_url = "https://www.avalonaccess.com/Information/Information/AmenityReservation?amenityKey=994bfb94-5b64-4efb-8f1a-601f9a935e6c"
	else: print("You must pick new or old for the fist argument"); return None

	if (num_ppl == '2') and (facility == 'new'): resv_list = [2, 'Andrei Kvasov, Alsu Kvasova']
	elif num_ppl == '1': resv_list = [1, 'Andrei Kvasov']
	else: print("You must pick 1 or 2, old center can not have 2 visitors!"); return None
	if time_arg_1.split(':')[0] == '11':
		my_time_1 = time_arg_1.split(':')[0] + ":00" + ' ' + 'AM' + " - " + time_arg_1.split(':')[1][:-2] + ':00' + ' ' + time_arg_1[-2:].upper()
	else: my_time_1 = time_arg_1.split(':')[0] + ":00" + ' ' + time_arg_1[-2:].upper() + " - " + time_arg_1.split(':')[1][:-2] + ':00' + ' ' + time_arg_1[-2:].upper()
	if time_arg_2.split(':')[0] == '11':
		my_time_2 = time_arg_2.split(':')[0] + ":00" + ' ' + 'AM' + " - " + time_arg_2.split(':')[1][:-2] + ':00' + ' ' + time_arg_2[-2:].upper()
	else: my_time_2 = time_arg_2.split(':')[0] + ":00" + ' ' + time_arg_2[-2:].upper() + " - " + time_arg_2.split(':')[1][:-2] + ':00' + ' ' + time_arg_2[-2:].upper()
	#####################################################################
	my_time_pointer = None
	avail_pointer = None
	driver = webdriver.Firefox()
	driver.get(avalon_url)
	wait=ui.WebDriverWait(driver,10)
	wait.until(page_is_loaded)
	#####################################################################
	today =  datetime.date.today()
	tomorrow = today + datetime.timedelta(days = 1)
	tomorrow_str = str(tomorrow)
	tomorrow_day = tomorrow_str.split('-')[2].lstrip("0")
	tomorrow_month = tomorrow.strftime("%b")
	######################Login######################################
	user = driver.find_element_by_name("UserName")
	password = driver.find_element_by_name("password")
	user.clear()
	user.send_keys("andrew.kvasoff@gmail.com")
	password.clear()
	password.send_keys("Oladuchek1986")
	driver.find_element_by_xpath('//button[@class="submit"]').click()
	time.sleep(6)
	#####Web form######################################################
	#############Select month###########################################
	driver.find_element_by_id('resv-date').click()
	to_month = driver.find_element_by_xpath("//div/select[@class='ui-datepicker-month']")
	selected_to_month=Select(to_month)
	selected_to_month.select_by_visible_text(tomorrow_month)
	time.sleep(2)
        #############Select date###########################################
	elements = driver.find_elements_by_xpath(".//*[@id='ui-datepicker-div']/table/tbody/tr/td/a") 
	for dates in elements:		
		if(dates.is_enabled() and dates.is_displayed() and str(dates.get_attribute("innerText")) == tomorrow_day):
		    dates.click()
	time.sleep(2)
	#########Select time from drop-down#################################
	time.sleep(2)
	#driver.find_element_by_css_selector("#SelStartTime [value='Thursday-7:00 PM-8:00 PM ']").click()

	inputs = ui.Select(driver.find_element_by_css_selector('#SelStartTime'))
	#option.get_attribute('value') 
	if my_time_1 > my_time_2:
		my_time_pointer = True
	for option in inputs.options:
		avail_date = str(option.text)
		if avail_date == "There are no available start times": driver.quit(); time.sleep(4); sys.exit(1)
		if my_time_pointer and my_time_2 in avail_date:
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
		if not avail_pointer: driver.quit(); time.sleep(4); sys.exit(1)

	time.sleep(4)
	##########################################################################
	driver.find_element_by_id('NumberOfPeople').send_keys(Keys.BACKSPACE)
	driver.find_element_by_id('NumberOfPeople').send_keys(resv_list[0])
	time.sleep(2)
	driver.find_element_by_id('ReservationNames').send_keys(resv_list[1])
	time.sleep(3)
	#reservation-terms - checkbox
	driver.find_element_by_id('reservation-terms').click()
	time.sleep(4)
	driver.find_element_by_id('submit-new-reservation').click() #Change to submit-new-reservation
	return True

if __name__ == '__main__':
	#######################################Help for script users################################################################################
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='''

	Usage:
 
	python ./avalon.py <old/new> <# of people: 1/2> <pref_time1> <pref_time2>

	Usage examples:

	python avalon.py new 2 4:5pm 5:6pm
	
			'''	
		)	
	parser.add_argument('strings',metavar='avalon_center',type=str,help=
		'''
		Old or New Fitness Center to book
		''')
	parser.add_argument('strings',metavar='num_of_people',type=int,help=
		'''
		 Number of people to visit the center
		''')
	parser.add_argument('strings',metavar='my_time_1',type=str,help=
		'''
	 	Preffered time to book the center
		''')
	parser.add_argument('strings',metavar='my_time_2',type=str,help=
		'''
	 	The second preffered time to book the center
		''')
	args=parser.parse_args()

	if (len(sys.argv)<4 or len(sys.argv)>5):
		print ("Incorrect arguments number. Must be 4")
		parser.print_usage()
		sys.exit(1)

	avalon_resv(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	
