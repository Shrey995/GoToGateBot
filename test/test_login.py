import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

class TestLoginWithSecondGoogleAccount(unittest.TestCase):
    screenshot_dir = "reports"  # The base directory for screenshots

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        # Find the last folder number in the "reports" directory
        existing_folders = [f for f in os.listdir(self.screenshot_dir) if f.startswith("test")]
        if existing_folders:
            latest_folder = max(existing_folders)
            latest_folder_number = int(latest_folder.split("_")[0][4:])
        else:
            latest_folder_number = 0

        self.test_case_count = latest_folder_number + 1  # Increment test case count
        self.test_dir = os.path.join(self.screenshot_dir, f"test{self.test_case_count}_screenshots")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        self.driver.save_screenshot(os.path.join(self.test_dir, f"{str(int(time.time()))}.png"))

    def test_login_with_second_google_account(self):
        self.driver.get("https://www.gotogate.com/")

        # Capture screenshot
        self.driver.save_screenshot(os.path.join(self.test_dir, "step1.png"))


        # Switch to your iframe by finding it using the "#document" identifier
        try:
            # iframe = WebDriverWait(self.driver, 10).until(
            #     EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@name='#document']"))
            # )

            # Find the element with class "g_id_signin" and click it
            element_to_click = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "g_id_signin"))
            )
            element_to_click.click()
            
            # Now the Google login page should automatically open in a new window/tab
            # Switch to the newly opened window/tab
            self.driver.switch_to.window(self.driver.window_handles[-1])

            # Capture screenshot after clicking the login button
            self.driver.save_screenshot(os.path.join(self.test_dir, "step3.png"))

            # Read the credentials from input.txt
            with open("inputs/input.txt", "r") as file:
                credentials = json.load(file)
            
            # Find and fill the email field
            email_field = self.driver.find_element(By.ID, "identifierId")
            email_field.send_keys(credentials["username"])
            
            # Capture screenshot after filling the email field
            self.driver.save_screenshot(os.path.join(self.test_dir, "step4.png"))

            # Click the "Next" button
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            
            # Wait for the password field to appear
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            
            # Fill the password field with the app password
            password_field.send_keys(credentials["password"])
            
            # Capture screenshot after filling the password field
            self.driver.save_screenshot(os.path.join(self.test_dir, "step5.png"))
            
            # Click the "Next" button to login
            next_button = self.driver.find_element(By.ID, "passwordNext")
            next_button.click()

            # Check for a successful login condition, e.g., presence of a specific element
            # You may need to modify this condition based on your application
            success_condition = EC.presence_of_element_located((By.ID, "success_element_id"))
            if not WebDriverWait(self.driver, 10).until(success_condition):
                self.fail("Login unsuccessful. Test failed.")

            # Optional: Add assertions or further test steps after logging in
            time.sleep(10)  # Adjust sleep time for further actions

            # Switch back to the original window/tab
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as e:
            self.fail(f"An error occurred while logging in: {str(e)}")  # Fail the test if there's an exception

if __name__ == "__main__":
    unittest.main()
