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

        print("Waiting for the page to load....")
        time.sleep(5)

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


    def update_attributes(self, attributes):
        existing_features, existing_labels = self.load_training_data()
        locator_type_, locator_value_ = next(iter(attributes.items()))


        # Extract the page source for training data
        page_source = self.driver.page_source
        existing_features.append(page_source)
        existing_labels.append(attributes)

        # Train the model with updated data
        self.train_model(existing_features, existing_labels)

        # Predict the best locator based on the current webpage
        predicted_locator = self.predict_locator(page_source)

        print(f"New predicted locator: {predicted_locator}")

        new_att={predicted_locator:locator_value_}

        print(new_att)
        exit()

        return new_att

    def train_model(self, features, labels):
        vectorizer = TfidfVectorizer()
        features_transformed = vectorizer.fit_transform(features)

        label_encoder = LabelEncoder()
        # Convert labels to strings
        y_train_encoded = label_encoder.fit_transform(list(map(str, labels)))

        model = MultinomialNB()
        model.fit(features_transformed, y_train_encoded)

        with open('locator_model.pkl', 'wb') as model_file:
            pickle.dump((vectorizer, model, label_encoder), model_file)

    def predict_locator(self, features):
        with open('locator_model.pkl', 'rb') as model_file:
            vectorizer, model, label_encoder = pickle.load(model_file)

        features_transformed = vectorizer.transform([features])
        prediction = model.predict(features_transformed)

        # Reverse the encoding to get the original locator
        predicted_locator = label_encoder.inverse_transform(prediction)

        return predicted_locator[0]

    def find_element(self, predicted_locator):
        try:
            element = self.driver.find_element(By.XPATH, predicted_locator)
            return element
        except Exception as e:
            print(f"Element not found with locator: {predicted_locator}. Exiting. Error: {e}")
            return None

    def load_training_data(self):
        existing_features, existing_labels = [], []

        if os.path.exists('data/training_data.csv'):
            df = pd.read_csv('data/training_data.csv')
            for index, row in df.iterrows():
                feature_values = [str(value) for value in row.values]
                feature_text = ' '.join(feature_values[1:])
                label_text = ''.join(feature_values[0])
                existing_features.append(feature_text)

                
                existing_labels.append(label_text)

        print("*"*20,existing_features)
        print("#"*20,existing_labels)

        return existing_features, existing_labels

    def save_training_data(self, features, labels):
        features_df = pd.DataFrame(features)
        labels_df = pd.DataFrame(labels)
        df = pd.concat([features_df, labels_df], axis=1)
        df.to_csv('data/training_data.csv', index=False, encoding='utf-8')

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

            self.click_button({'css': "input[type='submit']"})

            time.sleep(10)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()

        finally:
            self.driver.quit()

if __name__ == "__main__":
    automator = SelfHealingAutomation()
    automator.self_healing_script()
