import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import openai

class Scraper():
    def __init__(self):
        self.driver = webdriver.Chrome()
        try:
            self.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
        except KeyError:
            self.driver.close()
            raise KeyError("You must set environment variable OPENAI_API_KEY to your openai api key")
        """
        self.SELECTORS = {
            "class_name": By.CLASS_NAME, 
            "css_selector": By.CSS_SELECTOR, 
            "id": By.ID, 
            "name": By.NAME, 
            "link_text": By.LINK_TEXT, 
            "partial_link_text": By.PARTIAL_LINK_TEXT, 
            "tag_name": By.TAG_NAME, 
            "xpath": By.XPATH
        }
        """

    def download_website_html(self, url):
        """
        url: url to download
        selector: selenium selector (like By.CSS_SELECTOR)
        id: element to be selected (e.g if By.CSS_SELECTOR #fname)
        """
        #assert selector in self.SELECTORS.keys()

        #selector = self.SELECTORS[selector]

        self.driver.get(url)
        #self.driver.find_element(selector, id)

    def __del__(self):
        self.driver.close()
    