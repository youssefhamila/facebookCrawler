
import os
import googleapiclient.discovery
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
from DataExtraction import *


#scrolling parameters
current_scrolls = 0
scroll_time = 10
old_height = 0

#chromedriver options
def chromeOptions():
    options = webdriver.ChromeOptions()
    options.add_argument('lang=en')
    options.add_argument("window-size=1920,1080")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    return options
#check if new_height != old_height while scrolling
def check_height(driver):
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height
# scroll n times (parameter) 
def scroll(driver,total_scrolls):
    global old_height
    current_scrolls = 0
    closed=False
    while (True):
        try:
            
            if current_scrolls == total_scrolls:
                return
            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            if not closed:
                time.sleep(3)
                closed=closePopup(driver=driver)
            WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height(driver))
            current_scrolls += 1            
        except TimeoutException:
            break

    return
# scroll to bottom if no parameter is passed
def scrollall(driver):
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    closed=False
 
    while(match==False):
        oldclosed=False
        if not closed:
            time.sleep(3)
            closed=closePopup(driver)
            oldclosed=True
        if oldclosed== False:

            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True
# close login popup to continue scrolling
def closePopup(driver):
    try:
        but=driver.find_element_by_css_selector("div[class='cypi58rs pmk7jnqg fcg2cn6m tkr6xdv7']")
        ActionChains(driver).click(but).perform()
        return True
    except:
        try:
            but=driver.find_element_by_css_selector("div[aria-label='Close']")
            ActionChains(driver).click(but).perform()       
            return True 
        except:
            try:
                but=driver.find_element_by_css_selector("div[class='oajrlxb2 qu0x051f esr5mh6w e9989ue4 r7d6kgcz nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x i1ao9s8h esuyzwwr f1sip0of abiwlrkh p8dawk7l lzcic4wl bp9cbjyn s45kfl79 emlxlaya bkmhp75w spb7xbtv rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv j83agx80 taijpn5t jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 tv7at329 thwo4zme tdjehn4e']")
                ActionChains(driver).click(but).perform()
                return True
            except:
                return False
   

# load the page and extract the dom
def AccessUrl(url,scrol=-1):
    options=chromeOptions()
    driver = webdriver.Chrome('chromedriver',options=options)
    driver.maximize_window()
    driver.get(url)
    if scrol==-1:
        scrollall(driver)
    else:
        scroll(driver,scrol)
    html = bs(driver.page_source, "lxml")
    Posts(html)
    driver.close()