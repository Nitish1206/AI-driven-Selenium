
"""This file will Help you to update data to the website"""
#import required libraries
from lib2to3.pgen2 import driver
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import json 
import time
import traceback
import os
from selenium.webdriver.support.ui import Select

class AutomateTesting:
    def __init__(self,name="demo",address="demo",phonenumber="000000000",dob="1/1/2000",gender="Male",fathername="demo",):

        """init method is used to intialise class attributes 
        Args:
            search_jobtitle (String): Give job title which you want to search on naukri.com
            search_experience (int, optional): Filter for number of years of experience which you want search. Defaults to 0.
            search_location (str, optional): Filter for location of job. Defaults to "Pune".
            Disable_search_filter (Bool, optional): False will enable filter search. Defaults to "True".
        """
        
        # set chrome paramters and initialise url to search for scrapping
        self.set_chrome_parameter()
        self.url=" http://127.0.0.1:5000"
        self.driver.get(self.url)

        #initialise search parameters
        self.name = name
        self.address = address  
        self.phonenumber = phonenumber
        self.dob = dob
        self.gender = gender
        self.fathername=fathername
        

        print("wait for page to load....")
        time.sleep(5)
        self.updapte_input_field()
    
    
    def set_chrome_parameter(self):
        """
        set parameters for chrome like want to run on headless, window size for chrome, certification.....
        """
        chromedriver_autoinstaller.install()  
        """Check if the current version of chromedriver exists
        and if it doesn't exist, download it automatically,
        then add chromedriver to path"""
       
        self.chrome_options = webdriver.ChromeOptions()    
        # Add your options as needed    
        self.options = [
                            # Define window size here
                            "--window-size=1200,1200",
                            "--ignore-certificate-errors"
                            "--headless",
                            
                        ]
        for option in self.options:
            self.chrome_options.add_argument(option)
        
        # driver is used to drive a browser natively
        self.driver = webdriver.Chrome(options = self.chrome_options)

    
    def updapte_input_field(self):
        # Fill in the Name field
        # name_input = self.driver.find_element(By.NAME, "name")
        att=[By.NAME, "name"]
        name_input = self.driver.find_element(att[0],att[1])
        print("===>>>",name_input.get_attribute('outerHTML'))
        name_input.send_keys("Nitish")

        # Fill in the Address field
        address_input = self.driver.find_element(By.ID, "address")
        address_input.send_keys("Your Address")

        # Fill in the Phone Number field
        phone_number_input = self.driver.find_element(By.ID, "phone-number")
        phone_number_input.send_keys("Your Phone Number")

        # Fill in the Date of Birth field
        dob_input = self.driver.find_element(By.ID, "dob")
        dob_input.send_keys("06/12/1998")

        # Select gender from dropdown
        gender_input = Select(self.driver.find_element(By.ID, "gender"))
        gender_input.select_by_value("Male")  # Replace with the desired gender value

        # Fill in the Father's Name field
        father_name_input = self.driver.find_element(By.ID, "father-name")
        father_name_input.send_keys("Father's Name")

        # Fill in the Mother's Name field
        mother_name_input = self.driver.find_element(By.ID, "mother-name")
        mother_name_input.send_keys("Mother's Name")

        # Click the Submit button
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        time.sleep(10)
        self.udpate_feedback()

    def udpate_feedback(self):

        # Fill in the Name field
        name_input = self.driver.find_element(By.ID, "name")
        name_input.send_keys("Nitish")

        # Fill in the email field
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("demo@email.com")

        # Fill in the feedback field
        feedback_input = self.driver.find_element(By.ID, "feedback")
        feedback_input.send_keys("Hi there this is feedback")

        # Click the Submit button
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()

        time.sleep(10)



if __name__=="__main__":

    scrapper_object=AutomateTesting()