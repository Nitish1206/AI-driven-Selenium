import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import pickle
import os
import chromedriver_autoinstaller
import time
import traceback
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import re
from collections import Counter
import sys

# Regular expression pattern to find words
WORD = re.compile(r"\w+")

class SourcePageData:
    def __init__(self, path="data/training1.csv"):

        """init method is used to initialise class attributes """

        # Set chrome parameters and initialize the URL to search for scraping
        self.set_chrome_parameter()
        self.url = " http://127.0.0.1:5000"
        self.driver.get(self.url)
        self.data_path=path
        print("Waiting for the page to load....")
        time.sleep(5)
        self.create_training_data()

    def set_chrome_parameter(self):
        # Install ChromeDriver if not installed and set Chrome options
        chromedriver_autoinstaller.install()
        self.chrome_options = webdriver.ChromeOptions()
        self.options = [
            "--window-size=1200,1200",
            "--ignore-certificate-errors",
                            "--headless",

        ]

        for option in self.options:
            self.chrome_options.add_argument(option)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def create_training_data(self):
        page_source = self.driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        all_elements = soup.find_all(['label', 'input', 'select'])

        # Extract information from all elements on the page
        element_info_list = [self.extract_element_info(element) for element in all_elements]
        df = pd.DataFrame.from_dict(element_info_list)
        df.to_csv(self.data_path)

    def extract_element_info(self, element):
        # Extract information from a web element
        info = {
            "element": element.name,
            "tag": element.name if element.name != "none" else "none",
            "type": element.get('type', 'none'),
            "id": element.get('id', 'none'),
            "name": element.get('name', 'none'),
            "text": element.text.strip(),
            "value": element.get('value', 'none'),
            "for": element.get('for', 'none')
        }
        return info


if __name__=="__main__":

    scrapper_object=SourcePageData()