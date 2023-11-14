import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

class SelfHealingAutomation:
    def __init__(self, name="demo", address="demo", phonenumber="000000000", dob="1/1/2000", gender="Male", fathername="demo", mothername="demo",
                 email="demo@gmail.com"):

        """init method is used to initialise class attributes """

        # Set chrome parameters and initialize the URL to search for scraping
        self.set_chrome_parameter()
        self.url = " http://127.0.0.1:5000"
        self.driver.get(self.url)

        # Initialize search parameters
        self.name = name
        self.address = address
        self.phonenumber = phonenumber
        self.dob = dob
        self.gender = gender
        self.fathername = fathername
        self.mothername = mothername
        self.email = email
        self.feedback = "Hi there this is demo for testing automation using AI"

        self.existing_df = None
        print("Waiting for the page to load....")
        time.sleep(5)

    def set_chrome_parameter(self):
        # Install ChromeDriver if not installed and set Chrome options
        chromedriver_autoinstaller.install()
        self.chrome_options = webdriver.ChromeOptions()
        self.options = [
            "--window-size=1200,1200",
            "--ignore-certificate-errors",
        ]

        for option in self.options:
            self.chrome_options.add_argument(option)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def update_form(self, attributes, value="Default", Dtype="input"):
        try:
            print("*" * 50, attributes)

            # Create a locator and find the input field
            locator, lvalue = self.create_locator(attributes)
            input_field = self.driver.find_element(locator, lvalue)

            # Update the input field based on the specified Dtype
            if Dtype == "input":
                input_field.send_keys(value)
            if Dtype == "button":
                input_field.click()
            if Dtype == "option":
                selected_input = Select(input_field)
                selected_input.select_by_value(value)

        except Exception as e:
            print(f"Element not found with attributes: {attributes}. Trying to adapt...")
            new_attributes = self.update_attributes(attributes)
            if new_attributes:
                self.update_form(new_attributes, value=value, Dtype=Dtype)
            else:
                print(f"Unable to find element. Exiting. Error: {e}")

    def create_locator(self, attributes):
        try:
            print(attributes)

            # Extract locator type and value from attributes
            locator_type, locator_value = next(iter(attributes.items()))

            # Choose the appropriate locator type based on the input
            if locator_type.lower() == 'name':
                return [By.NAME, locator_value]
            elif locator_type.lower() == 'id':
                return [By.ID, locator_value]
            elif locator_type.lower() == 'xpath':
                return [By.XPATH, locator_value]
            elif locator_type.lower() == 'css_selector':
                return [By.CSS_SELECTOR, locator_value]
            # Add more cases for other locator types as needed
            else:
                raise ValueError(f"Unsupported locator type: {locator_type}")

        except Exception as e:
            print(f"Unable to find locator. Error: {e}")

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

    def update_attributes(self, attributes):
        existing_features, existing_labels = self.load_training_data()

        # Extract the page source for training data
        page_source = self.driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        all_elements = soup.find_all(['label', 'input', 'select', 'option'])

        # Extract information from all elements on the page
        element_info_list = [self.extract_element_info(element) for element in all_elements]
        df = pd.DataFrame.from_dict(element_info_list)

        updated_feature = self.update_training_data(df)

        locator_type_, locator_value_ = next(iter(attributes.items()))

        print("*" * 15, locator_type_)
        print("*" * 15, locator_value_)

        # Find rows in the existing DataFrame based on locator type and value
        label_address_rows = self.existing_df[self.existing_df[locator_type_] == locator_value_]
        test_list = label_address_rows.values.tolist()[0]
        test_text = ' '.join(test_list)

        print("#" * 15, test_text)

        test_vec = self.text_to_vector(test_text)

        # Predict the best locator based on the current webpage
        key, score = self.predict_locator(test_vec, updated_feature)

        predicted_locator_value = df.iloc[key][locator_type_]
        predicted_locator = locator_type_

        print(f"New predicted locator: {predicted_locator}")
        print(f"New predicted locator: {predicted_locator}, Value: {predicted_locator_value}")
        updated_attribute = {predicted_locator: predicted_locator_value}

        # Store alert message in a variable
        alert_message = f"Not found! Locator:--> {locator_type_}, value:--> {locator_value_}, \\n\\nNew predicted locator:--> {predicted_locator}, Value:--> {predicted_locator_value}"

        # Show a custom alert when a new element is found with the stored message
        self.show_custom_alert(alert_message)

        try:
            # Wait for the alert to be present
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            print(f"Alert present: {alert_text}")
            time.sleep(6)
            alert.accept()  # Close the existing alert
        except Exception as e:
            # print("No alert present")
            pass

        return updated_attribute
    
    def show_custom_alert(self, message):
        # You can customize the styling of your custom alert here
        custom_alert_script = f"""
        var customAlert = document.createElement('div');
        customAlert.style.position = 'fixed';
        customAlert.style.top = '10%';
        customAlert.style.left = '50%';
        customAlert.style.transform = 'translate(-50%, -50%)';
        customAlert.style.backgroundColor = '#ffffff';
        customAlert.style.padding = '20px';
        customAlert.style.border = '2px solid #3498db';
        customAlert.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
        customAlert.style.zIndex = '1000';
        customAlert.style.borderRadius = '8px';
        customAlert.style.fontFamily = 'Arial, sans-serif';
        customAlert.style.maxWidth = '400px';
        customAlert.style.textAlign = 'center';
        customAlert.style.fontSize = '16px';  // Font size
        customAlert.innerText = '{message}';
        document.body.appendChild(customAlert);
        setTimeout(function() {{
            document.body.removeChild(customAlert);
        }}, 5000);  // Automatically remove the custom alert after 5 seconds
        """

        self.driver.execute_script(custom_alert_script)


    def text_to_vector(self, text, ):
        words = WORD.findall(text)
        return Counter(words)

    def get_cosine(self, vec1, vec2):
        # Calculate the cosine similarity between two vectors
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def predict_locator(self, test_feature, features):
        # Predict the best locator based on cosine similarity
        result_dict = {}
        for i, f1 in enumerate(features):
            cosine = self.get_cosine(f1, test_feature)
            result_dict[i] = cosine

        max_key = max(result_dict, key=lambda k: result_dict[k])
        max_value = result_dict[max_key]

        return max_key, max_value

    def update_training_data(self, df):
        # Update the training data with new features
        new_features, new_labels = [], []

        for index, row in df.iterrows():
            feature_values = [str(value) for value in row.values]
            feature_text = ' '.join(feature_values[1:])
            label_text = ''.join(feature_values[0])
            vec = self.text_to_vector(feature_text)
            new_features.append(vec)

        return new_features

    def load_training_data(self):
        # Load existing training data from a CSV file
        existing_features, existing_labels = [], []

        if os.path.exists('data/training_data.csv'):
            df = pd.read_csv('data/training_data.csv')
            self.existing_df = df

            for index, row in df.iterrows():
                feature_values = [str(value) for value in row.values]
                feature_text = ' '.join(feature_values[1:])
                label_text = ''.join(feature_values[0])
                existing_features.append(feature_text)
                existing_labels.append(label_text)

        return existing_features, existing_labels

    def index_page_testing(self):
        # Test the index page by updating various form fields
        self.update_form({'id': 'name'}, value=self.name)
        self.update_form({'id': 'address'}, value=self.address)
        self.update_form({'id': 'phone-number'}, value=self.phonenumber)
        self.update_form({'id': 'dob'}, value=self.dob)
        self.update_form({'id': 'gender'}, value=self.gender, Dtype="option")
        self.update_form({'id': 'father-name'}, value=self.fathername)
        self.update_form({'id': 'mother-name'}, value=self.mothername)
        self.update_form({'css_selector': "input[type='submit']"}, Dtype="button")

    def feedback_page_testing(self):
        # Test the feedback page by updating form fields
        self.update_form({'id': 'name'}, value=self.name)
        self.update_form({'id': 'email'}, value=self.email)
        self.update_form({'id': 'feedback'}, value=self.feedback)
        self.update_form({'css_selector': "input[type='submit']"}, Dtype="button")

    def self_healing_script(self):
        try:
            # Execute the self-healing script
            self.index_page_testing()
            time.sleep(10)
            self.feedback_page_testing()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()

        finally:
            # Quit the WebDriver
            self.driver.quit()

if __name__ == "__main__":
    # Create an instance of the SelfHealingAutomation class and run the self-healing script
    automator = SelfHealingAutomation()
    automator.self_healing_script()
