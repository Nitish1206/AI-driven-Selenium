from selenium.webdriver.common.by import By

class SelfHealingAutomation:
    # ... (rest of the code remains the same)

    def create_locator(self, attributes):
        locator_type, locator_value = next(iter(attributes.items()))

        if locator_type.lower() == 'name':
            return f'By.NAME, "{locator_value}"'
        elif locator_type.lower() == 'id':
            return f'By.ID, "{locator_value}"'
        elif locator_type.lower() == 'xpath':
            return f'By.XPATH, "{locator_value}"'
        # Add more cases for other locator types as needed
        else:
            raise ValueError(f"Unsupported locator type: {locator_type}")

# Example of how to use create_locator
automator = SelfHealingAutomation()
locator = automator.create_locator({'name': 'your_element_name'})
print(locator)