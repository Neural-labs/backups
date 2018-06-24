    import selenium.webdriver
import json
import re
import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from pymongo import MongoClient

#conn = MongoClient("mongodb://Rex:12345678@localhost")
conn = MongoClient("mongodb://rex:groupten123!@34.193.29.224")
Recruiters = conn.Recruiters
Info = Recruiters.Info
URL = Recruiters.URL

def access(fromPage=1, toPage=4743):
	driver = selenium.webdriver.Chrome(executable_path="C:\\chromedriver.exe")

	handshakeURL = "https://app.joinhandshake.com/login"
	driver.get(handshakeURL)
	
	emailAddress = driver.find_element_by_class_name("login-main__input")
	emailAddress.send_keys("jsn76@cornell.edu")
	emailAddress.send_keys(Keys.RETURN)

	loginButton = driver.find_element_by_xpath("//a[@class='btn login__btn--primary']")
	loginButton.click()

	username = driver.find_element_by_id("netid")
	password = driver.find_element_by_id("password")
	
	username.send_keys("jsn76")
	password.send_keys("@G!nes16")
	password.send_keys(Keys.RETURN)
	
	#employerURL = "https://cornell.joinhandshake.com/employers"
	employerURL = "https://cornell.joinhandshake.com/employers?ajax=true&query=&category=Employer&page="+str(fromPage)+"&per_page=25&sort_direction=asc&sort_column=default&followed_only=false&qualified_only=&core_schools_only=false&including_all_facets_in_searches=false"
	driver.get(employerURL)
	pageCount = fromPage

	while 1:
		print "###################"
		print "page: " + str(pageCount)
		print "###################"
		time.sleep(3)
		currentPageUrl = driver.current_url
		if pageCount >= fromPage:
			try:
				fetchCurrentEmployersPage(driver)
			except Exception as e:
				print e
				print "Fetal!!"
				print driver.current_url
				print "go back!"
				driver.get(currentPageUrl)
				time.sleep(2)
		time.sleep(2)
		nextPageEle = driver.find_element_by_xpath('//div[@class="control next-page"]')
		nextPageEle.click()
		pageCount += 1

		if pageCount > toPage:
			break

def fetchCurrentEmployersPage(driver):
	currentID = 0
	employersEleList = driver.find_elements_by_xpath("//h5[@class='feed-title inline-block']")
	employersEleListLen = len(employersEleList)

	while 1:
		scrollTopPos = currentID * 100
		js="var q=document.documentElement.scrollTop=" + str(scrollTopPos)
		driver.execute_script(js)
		employerEle = employersEleList[currentID]
		employerEle.click()
		time.sleep(2)
		try:
			analyzeSingleEmployerPage(driver)
		except Exception as e:
			print e
			print "Something wrong in this page: " + driver.current_url
		driver.back()
		time.sleep(3)
		currentID += 1
		employersEleList = driver.find_elements_by_xpath("//h5[@class='feed-title inline-block']")
		
		if employersEleListLen == currentID:
			break

		if len(employersEleList) != employersEleListLen:
			driver.refresh()
			time.sleep(5)
			employersEleList = driver.find_elements_by_xpath("//h5[@class='feed-title inline-block']")


def analyzeSingleEmployerPage(driver):
	time.sleep(1.5)
	try:
		name = driver.find_element_by_xpath('//h3[@class="profile-page-section-header"]').text
		name = re.sub(r'About ', '', name)
		description = driver.find_element_by_xpath('//div[@class="well respect-newlines"]').text
	except Exception as e:
		print "Unqualified Item!"
		return 0

	try:
		brief = driver.find_element_by_xpath('//p[@class="margin-top"]').text
	except Exception as e:
		# print e
		brief = ""
	
	try:
		picurl = driver.find_element_by_xpath('//img[@class="img-thumbnail max-width150"]').get_attribute('outerHTML')
		picurl = re.sub(r'<img[\w\W]*?src=\"', '', picurl)
		picurl = re.sub(r'\">', '', picurl)

	except Exception as e:
		# print e
		picurl = ""

	detailedEleList = driver.find_elements_by_xpath('//div[@class="entity-sidebar tile white"]/div[@class="property-box"]')
	location = ""
	industry = ""
	size = ""
	type_ = ""
	for detailedEle in detailedEleList:
		detailedHTML = detailedEle.get_attribute('outerHTML')
		detailedName = re.sub(r'[\w\W]*<h4>', '', detailedHTML)
		detailedName = re.sub(r'</h4>[\w\W]*', '', detailedName)
		detailedContent = re.sub(r'[\w\W]*<span>', '', detailedHTML)
		detailedContent = re.sub(r'</span>[\w\W]*', '', detailedContent)
		
		if detailedName.lower() == "location":
			location = detailedContent
		elif detailedName.lower() ==  "industry":
			industry = detailedContent
		elif detailedName.lower() ==  "size":
			size = detailedContent
		elif detailedName.lower() == "type":
			type_ = detailedContent
		else:
			print "??????????????????????"
			print "UNKNOWN ATTRIBUTE!!!!!"
			print "??????????????????????"

	"""
	try:
		location = driver.find_element_by_xpath('//div[@class="entity-sidebar tile white"]/div[@class="property-box"][1]/span').text
	except Exception as e:
		# print e
		location = ""

	try:
		industry = driver.find_element_by_xpath('//div[@class="entity-sidebar tile white"]/div[@class="property-box"][2]/span').text
	except Exception as e:
		# print e
		industry = ""

	try:	
		size = driver.find_element_by_xpath('//div[@class="entity-sidebar tile white"]/div[@class="property-box"][3]/span').text
	except Exception as e:
		# print e
		size = ""
	"""
	
	try:
		website = driver.find_element_by_xpath('//div[@class="entity-sidebar tile white"]/div[last()-1]/div[@class="property-box"][1]/span').text
	except Exception as e:
		# print e
		website = ""

	try:
		phone = driver.find_element_by_xpath('//div[@class="entity-sidebar tile white"]/div[last()-1]/div[@class="property-box"][2]/span').text
	except Exception as e:
		# print e
		phone = ""

	try:
		email = driver.find_element_by_xpath('//div[@class="entity-sidebar tile white"]/div[last()-1]/div[@class="property-box"][3]/span').text
	except Exception as e:
		# print e
		email = ""
	
	url  = driver.current_url
	item = {}
	item["name"] = name
	item["description"] = description
	item["location"] = location
	item["industry"] = industry
	item["size"] = size
	item["website"] = website
	item["phone"] = phone
	item["email"] = email
	item["picurl"] = picurl
	item["brief"] = brief
	item["url"] = url
	item["type"] = type_
	feedData(item)

def feedData(item):
	Info.insert(item)
	urlItem = {"url":item["url"]}
	URL.insert(urlItem)
	print "Insert: " + item["name"]

if __name__ == '__main__':
	access(fromPage=260)
 