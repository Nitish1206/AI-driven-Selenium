# AI Driven Automation Testing

<p class="has-line-data" data-line-start="0" data-line-end="1">This repository contains a Python script for a self-healing automation system using AI-driven testing. The script utilizes Selenium for web automation, BeautifulSoup for HTML parsing, and similarity matrix. The self-healing aspect is achieved through the prediction of updated locators based on the current webpage structure.</p>
<p class="has-line-data" data-line-start="2" data-line-end="4">Installation<br>
Before running the script, ensure you have the necessary dependencies installed. You can install them using the following commands:</p>
<p class="has-line-data" data-line-start="5" data-line-end="9">pip install beautifulsoup4<br>
pip install chromedriver-autoinstaller<br>
pip install flask<br>
pip install selenium</p>
<p class="has-line-data" data-line-start="10" data-line-end="12">Clone the Repository:<br>
git clone <a href="https://github.com/Nitish1206/AI-driven-Selenium.git">https://github.com/Nitish1206/AI-driven-Selenium.git</a></p>
<p class="has-line-data" data-line-start="13" data-line-end="17">cd webapp<br>
Run the Script:<br>
Execute the flask_app.py script<br>
python flask_app.py</p>
<p class="has-line-data" data-line-start="18" data-line-end="22">cd automation_script<br>
Run the Script:<br>
Execute the ai_driven_testing.py script<br>
python ai_driven_testing.py</p>
<p class="has-line-data" data-line-start="23" data-line-end="24">This will initiate the self-healing automation process on a local Flask web application. The script will automatically interact with the webpage, updating form fields and predicting new locators if needed.</p>
<p class="has-line-data" data-line-start="25" data-line-end="28">Configuration<br>
Web Application URL:<br>
The script is set to interact with a local Flask web application. Update the url variable in the script if your application is hosted elsewhere.</p>
<p class="has-line-data" data-line-start="29" data-line-end="31">Default User Data:<br>
The script is initialized with default user data for form fields. You can customize the user details in the SelfHealingAutomation class constructor.</p>
<p class="has-line-data" data-line-start="32" data-line-end="35">Folder Structure<br>
data/: Contains the training data CSV file.<br>
ai_driven_testing.py: The main Python script for self-healing automation.</p>
<p class="has-line-data" data-line-start="36" data-line-end="37"><img src="results/automation_test.jpeg" alt="result"></p>
<p class="has-line-data" data-line-start="38" data-line-end="42">Acknowledgments<br>
Inspired by the concept of self-healing automation in software testing.<br>
Libraries used: Flask, Selenium, BeautifulSoup, scikit-learn.<br>
Feel free to explore and modify the script to suit your specific testing needs. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request. Happy testing!</p>