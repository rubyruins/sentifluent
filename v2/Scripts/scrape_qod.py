import bs4 as bs
import lxml
from urllib.request import Request, urlopen
import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException

url = "https://www.wattpad.com/story/112734148-queen-of-death-%E2%9C%94"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
sauce = urlopen(req).read()
soup = bs.BeautifulSoup(sauce,'lxml')
links = []

for item in soup.find_all('a'):
	item = item.get('href')
	item = str(item)
	item = "https://www.wattpad.com" + item
	links.append(item)
	
driver = webdriver.Chrome("..\chromedriver_win32\chromedriver.exe")

links = links[69:130]

def scrapey(i):
	driver.get(links[i])
	time.sleep(2)
	try:
		for i in range(500):
			time.sleep(1)
			find = driver.find_element_by_class_name('on-showmore')
			find.send_keys(Keys.ARROW_DOWN)
			try:
				driver.find_element_by_class_name('on-showmore').click()
			except:
				pass
	finally:
		print("Scrolled to bottom.")
		l = driver.find_elements_by_class_name('comment')
		c = driver.find_elements_by_xpath("//a[@href = '#']")[3].text
		r = driver.find_elements_by_xpath("//span[@class = 'reads']")[0].text
		v = driver.find_elements_by_xpath("//span[@class = 'votes']")[0].text
		title = driver.find_elements_by_class_name('panel')
		title = title[0].text.split('\n')[0]
		print(title)
		print("Comments found", len(l))
		print("Total comments", c)
		print("Total votes", v)
		print("Total reads", r)
		with open('..\Data\chapterdata_qod.csv', mode='a') as f:
			f.write("{},{},{},{},{}".format(c, len(l), r, v, title))
			f.write("\n")
		f.closed

		with open('..\Data\commentdata_qod.csv', mode='a', encoding='utf-8') as f:
			for i in l:
				mycomment = i.text.split('\n')
				mycomment.insert(0, title)
				comlen = len(mycomment)
				linesoftext = comlen - 5
				if comlen > 5:
					mycomment[3:comlen-1] = [' '.join(mycomment[3:comlen-1])]
					mycomment[3] = mycomment[3].replace(',', ' ')
				f.write("{},{},{},{}".format(mycomment[0], mycomment[1], mycomment[2], mycomment[3]))
				f.write("\n")
		print("Done writing")
		f.closed

for i in range(60, len(links)):
	try:
		scrapey(i)
	except ElementNotInteractableException:
		print("All done")

driver.close()