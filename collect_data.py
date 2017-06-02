import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from constants import *

driver = webdriver.Chrome("/Users/maruthgoyal/Downloads/chromedriver")

def main():

	regno = START_ROLL_NO
	conn = pymongo.MongoClient(DB_URL)
	db = conn[DB]

	while regno < MAX_ROLL_NO:
		print regno
		driver.get(URL)

		student_no_login = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td/center[2]/form/div[1]/center/table/tbody/tr[1]/td[2]/input")
		school_no_login = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td/center[2]/form/div[1]/center/table/tbody/tr[2]/td[2]/input")
		center_no_login = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td/center[2]/form/div[1]/center/table/tbody/tr[3]/td[2]/input")

		student_no_login.send_keys(str(regno))
		school_no_login.send_keys(SCHOOL_NO)
		center_no_login.send_keys(CENTER_NO)
		center_no_login.send_keys(Keys.RETURN)

		if ("Result Not Found" in driver.page_source or "Access denied" in driver.page_source):
			print "WHOOPS"
			regno += 1
			continue

		table = driver.find_element_by_xpath("/html/body/div[1]/div/center/table/tbody")
		tr_s = "tr[%d]"

		
		i = 2
		
		while True:
			print i

			row = table.find_element_by_xpath(tr_s % i)
			subject = row.find_element_by_xpath("td[2]").text.strip().lower()
			marks = row.find_element_by_xpath("td[5]").text.strip()


			if marks.isdigit():
				marks = int(marks)
			else:
				break

			db[subject].insert_one({"marks": marks})

			i += 1

		regno += 1
		

main()