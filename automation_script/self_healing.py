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

import math
import re
from collections import Counter

WORD = re.compile(r"\w+")

class SelfHealingAutomation:
    def __init__(self, name="demo", address="demo", phonenumber="000000000", dob="1/1/2000", gender="Male", fathername="demo"):
        self.set_chrome_parameter()
        self.url = "http://127.0.0.1:5000"
        self.driver.get(self.url)

        self.name = name
        self.address = address
        self.phonenumber = phonenumber
        self.dob = dob
        self.gender = gender
        self.fathername = fathername
        self.existing_df=None
        print("Waiting for the page to load....")
        time.sleep(5)

        self.self_healing_script()

    def set_chrome_parameter(self):
        chromedriver_autoinstaller.install()
        self.chrome_options = webdriver.ChromeOptions()
        self.options = [
            "--window-size=1200,1200",
            "--ignore-certificate-errors",
            # "--headless",
        ]
        for option in self.options:
            self.chrome_options.add_argument(option)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def update_input_field(self, attributes, value):
        try:
            print("*"*50,attributes)
            # exit()
            locator,lvalue=self.create_locator(attributes)
            input_field = self.driver.find_element(locator,lvalue)
            # exit()
            input_field.send_keys(value)
        except Exception as e:
            print(f"Element not found with attributes: {attributes}. Trying to adapt...")
            traceback.print_exc()
            new_attributes = self.update_attributes(attributes)
            if new_attributes:
                self.update_input_field(new_attributes, value)
            else:
                print(f"Unable to find element. Exiting. Error: {e}")
                exit()

    def create_locator(self, attributes):
        try:
            
            print(attributes)
            locator_type, locator_value = next(iter(attributes.items()))

            if locator_type.lower() == 'name':
                return [By.NAME, locator_value]
            elif locator_type.lower() == 'id':
                print("inside id")
                return [By.ID, locator_value]
            elif locator_type.lower() == 'xpath':
                return [By.XPATH, locator_value]

            elif locator_type.lower() == 'css_selector':
                return [By.CSS_SELECTOR, locator_value]
            # Add more cases for other locator types as needed
            else:
                raise ValueError(f"Unsupported locator type: {locator_type}")
        except:
            traceback.print_exc()

            exit()
    
    def click_button(self, attributes):
        try:
            locator_type, locator_value = next(iter(attributes.items()))
            locator,lvalue=self.create_locator(attributes)

            button = self.driver.find_element(locator,lvalue)
            button.click()
        except Exception as e:
            print(f"Button not found with locator: {locator}. Exiting. Error: {e}")

    def extract_element_info(self,element):
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

    def update_attributes(self, attributes):
        existing_features, existing_labels = self.load_training_data()

        # Extract the page source for training data
        page_source = self.driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        all_elements = soup.find_all(['label', 'input', 'select', 'option'])

        element_info_list = [self.extract_element_info(element) for element in all_elements]
        df = pd.DataFrame.from_dict(element_info_list)

        updated_feature = self.update_training_data(df)

        locator_type_, locator_value_ = next(iter(attributes.items()))

        print("*"*15,locator_type_)
        print("*"*15,locator_value_)

        label_address_rows = self.existing_df[self.existing_df[locator_type_] == locator_value_]
        test_list=label_address_rows.values.tolist()[0]
        test_text = ' '.join(test_list)

        print("#"*15,test_text)

        test_vec=self.text_to_vector(test_text)

        # Predict the best locator based on the current webpage
        key,score = self.predict_locator(test_vec,updated_feature)

        predicted_locator_value=df.iloc[key][locator_type_]
        predicted_locator=locator_type_

        print(f"New predicted locator: {predicted_locator}")

        print(f"New predicted locator: {predicted_locator}, Value: {predicted_locator_value}")
        updated_attribute={predicted_locator : predicted_locator_value}


        return updated_attribute

    def text_to_vector(self,text,):
        words = WORD.findall(text)
        return Counter(words)

    def get_cosine(self,vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def predict_locator(self, test_feature,features):
        result_dict={}
        for i,f1 in enumerate(features):
            cosine = self.get_cosine(f1, test_feature)
            result_dict[i]=cosine
        
        max_key = max(result_dict, key=lambda k: result_dict[k])
        max_value = result_dict[max_key]

        return max_key,max_value

    def find_element(self, predicted_locator):
        try:
            element = self.driver.find_element(By.XPATH, predicted_locator)
            return element
        except Exception as e:
            print(f"Element not found with locator: {predicted_locator}. Exiting. Error: {e}")
            return None

    def update_training_data(self,df):
        new_features, new_labels = [], []

        for index, row in df.iterrows():
                feature_values = [str(value) for value in row.values]
                feature_text = ' '.join(feature_values[1:])
                label_text = ''.join(feature_values[0])
                vec=self.text_to_vector(feature_text)
                new_features.append(vec)

        return new_features

    def load_training_data(self):
        existing_features, existing_labels = [], []

        if os.path.exists('data/training_data.csv'):
            df = pd.read_csv('data/training_data.csv')
            self.existing_df=df

            for index, row in df.iterrows():
                feature_values = [str(value) for value in row.values]
                feature_text = ' '.join(feature_values[1:])
                label_text = ''.join(feature_values[0])
                existing_features.append(feature_text)
                existing_labels.append(label_text)

        return existing_features, existing_labels


    def self_healing_script(self):
        try:
            self.update_input_field({'id': 'name'}, "Nitish")
            self.update_input_field({'id': 'address'}, "Your Address")
            self.update_input_field({'id': 'phone-number'}, "Your Phone Number")
            self.update_input_field({'id': 'dob'}, "06/12/1998")

            gender_input = Select(self.driver.find_element(By.ID, "gender"))
            gender_input.select_by_value("Male")

            self.update_input_field({'id': 'father-name'}, "Father's Name")
            self.update_input_field({'id': 'mother-name'}, "Mother's Name")

            self.click_button({'css_selector': "input[type='submit']"})

            time.sleep(10)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()

        finally:
            self.driver.quit()

if __name__ == "__main__":
    automator = SelfHealingAutomation()
    # automator.self_healing_script()
