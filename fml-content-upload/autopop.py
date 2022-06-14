import re
import time
import os
import platform
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

#checks OS version to determine which webdriver to use
if platform.system() == "Darwin":
	osversion="macos/geckodriver"
elif platform.system() == "Windows":
	osversion="windows/geckodriver.exe"
else:
	osversion="linux/geckodriver"

PATH = os.path.abspath("priv/webdriver/"+osversion)
driver = webdriver.Firefox(executable_path=PATH)

username=input("Enter Username")
password=input("Enter Password")

comp_name=['Karcher','Rustoleum','BFGoodrich','Chromagen','CRC','Crosby','Leo','Loncin','Michelin','Schulz','Senco','Shop Fox','Stihl','Swingtec','Rust-oleum','TechKing','Tigar','Victron Energy','Wood-Mizer']
prod_type=['Blower','Brushcutter','Chain Saw','Clearing saw','Cut Off Saw','Earth Auger','Hedge Trimmer','Mist Blower','Mower','Pressure Washer','Scrubber drier','Shredder','Spray-extraction cleaner','Steam cleaner','Sweeper','Tiller','Vacuum','Window Vac']
content_array = []
titline = []
imageline = []
imagenum=0
specnum=0

#stores each line from file in separate array index
with open('dropfileshere/compile.txt') as f:
		for line in f:
				content_array.append(line)

#removes blank lines
while("\n" in content_array) :
	content_array.remove("\n")

#stores the index locations of the delimiters to find the ranges in which the data for titles, descriptions, and specs are stored
for i in range(0,len(content_array)):
	if "zzz" in content_array[i]:
		titline.append(i)
		titline.append(i+1)
titline.append(len(content_array)) 

#Log-in Process
driver.get("https://fmlgy.com/user")
elem = driver.find_element_by_id("edit-name")
elem.send_keys(username)
elem = driver.find_element_by_id("edit-pass")
elem.send_keys(password)
elem = driver.find_element_by_id("edit-submit")
elem.click()

driver.get("https://fmlgy.com/node/add/product")
#identifies if the current line in the array is part of a title, description, or spec
for c in range(1,len(titline),2):
	for i in range(titline[c],titline[c+1]):
		#when c is in a title index (aka c = c + 0)
		if c%3 == 1:
			elem = driver.find_element_by_id("edit-title")
			elem.send_keys(content_array[i])
			print(content_array[i])
			for category in range(0,len(comp_name)):
				if comp_name[category].lower() in content_array[i].lower():
					select = Select(driver.find_element_by_name("field_product_brand[und]"))
					select.select_by_visible_text(comp_name[category])
					print (comp_name[category])
			for category in range(0,len(prod_type)):
				if prod_type[category].lower() in content_array[i].lower():
					select = Select(driver.find_element_by_name("field_product_category[und]"))
					select.select_by_visible_text(prod_type[category])
					print (prod_type[category])
		#when c is in a description index (aka c = c + 2)
		if c%3 == 0:
			elem = driver.find_element_by_id("edit-field-product-description-und-0-value")
			elem.send_keys(content_array[i])
			print(content_array[i])
		#when c is in a spec index (aka c = c + 4)
		if c%3 == 2:
			content_array[i] = re.split(r"\s{2,}", content_array[i])
			elem = driver.find_element_by_id("edit-field-product-specification-und-"+str(specnum)+"-value")
			elem.send_keys(content_array[i][0])
			elem = driver.find_element_by_id("edit-field-specification-unit-und-"+str(specnum)+"-value")
			elem.send_keys(content_array[i][1])
			elem = driver.find_element_by_name("field_product_specification_add_more")
			elem.click()
			elem = driver.find_element_by_name("field_specification_unit_add_more")
			elem.click()
			time.sleep(4)
			specnum=specnum+1
			print(content_array[i][0])
			print(content_array[i][1])

	#when all data for the current entry has been inputted
	if c%3 == 2:
		imagenum = imagenum+1
		imagepath=os.path.abspath("dropfileshere/image"+str(imagenum)+".png")
		elem = driver.find_element_by_id("edit-field-product-image-und-0-upload")
		elem.send_keys(imagepath)
		elem = driver.find_element_by_id("edit-submit")
		elem.click()
		time.sleep(4)
		print("image"+str(imagenum))
		print("saved\n\n\n")
		specnum = 0
		driver.get("https://fmlgy.com/node/add/product")
