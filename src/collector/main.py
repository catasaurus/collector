import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import openai

class Scraper():
    def __init__(self):
        self.driver = webdriver.Chrome()
        try:
            self.OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        except KeyError:
            self.driver.close()
            raise KeyError('You must set environment variable OPENAI_API_KEY to your openai api key')
        self.SELECTORS = {
            'class_name': By.CLASS_NAME, 
            'css_selector': By.CSS_SELECTOR, 
            'id': By.ID, 
            'name': By.NAME, 
            'link_text': By.LINK_TEXT, 
            'partial_link_text': By.PARTIAL_LINK_TEXT, 
            'tag_name': By.TAG_NAME, 
            'xpath': By.XPATH,
        }

    def download_website_html(self, url, selector, id):
        """
        url: url to download
        selector: selenium selector (like By.CSS_SELECTOR)
        id: element to be selected (e.g if By.CSS_SELECTOR #fname)
        """
        # TODO: add in support for performing several operations (maybe in user workflow allow user to do their own processing)
        assert selector in self.SELECTORS.keys()

        selector = self.SELECTORS[selector]
        #print(selector)

        self.driver.get(url)

        element = WebDriverWait(self.driver, timeout=4).until(lambda d: d.find_element(selector, id))
        html = element.get_attribute('innerHTML')

        return html
    
    def ai_completion(self, prompt, model, temp):
        completion = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temp
        )
        return [i["text"] for i in completion["choices"]]
    
    def process_html_ai(self, html, extract):
        """
        html: html to process (it may to long, if this is the case select a smaller element)
        extract: what to tell the model to extract
        """
        prompt = "Give me just the code (without any other text) for extracting " + extract + " from "
        prompt += html

        completion = self.ai_completion(prompt, 'text-davinci-003', 0.6)
        completion = completion[0].replace('\n', '')
        return completion
    
    def __del__(self):
        self.driver.close()
    