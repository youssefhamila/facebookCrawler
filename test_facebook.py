from selenium import webdriver
import unittest
from DataExtraction import *
from bs4 import BeautifulSoup as bs
from facebookCrawler import chromeOptions 
class FacebookTest(unittest.TestCase):
    def setUp(self) :
        self.driver = webdriver.Chrome('chromedriver',options=chromeOptions())
        self.driver.get("https://www.facebook.com/Meta/")
    def tearDown(self):
        self.driver.close()
    #test if posts html did not change
    def test_postExist(cls):
        html = bs(cls.driver.page_source, "lxml")
        cls.assertNotEqual(len(html.findAll("div",{"class":"du4w35lb l9j0dhe7"})),0)
    # test if page name is Meta
    def test_pageName(cls):
        html = bs(cls.driver.page_source, "lxml")
        cls.assertEqual(getPagename(html),"Meta")

if __name__ == '__main__':
    unittest.main()