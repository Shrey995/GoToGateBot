import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

class TestFlightBooking(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def take_screenshot(self, name):
        self.driver.save_screenshot(f"reports/{self.__class__.__name__}/{name}.png")

    def change_date_class(self, start_date_label, end_date_label, new_start_class, new_end_class):
        try:
            date_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[aria-label^="Sun "]'))
            )
            for date_element in date_elements:
                date_label = date_element.get_attribute("aria-label")
                if date_label == start_date_label:
                    self.driver.execute_script(f"arguments[0].setAttribute('class', '{new_start_class}');", date_element)
                elif date_label == end_date_label:
                    self.driver.execute_script(f"arguments[0].setAttribute('class', '{new_end_class}');", date_element)
        except Exception as e:
            self.fail(f"An error occurred while changing the class of the date elements: {str(e)}")

    def select_date(self, target_date):
        try:
            date_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[aria-label^="Sun "]'))
            )
            for date_element in date_elements:
                date_label = date_element.get_attribute("aria-label")
                if date_label == target_date:
                    date_element.click()
                    return True
            return False  # Date not found
        except Exception as e:
            self.fail(f"An error occurred while selecting the date: {str(e)}")

    def select_month_and_year(self, target_month, target_year):
        try:
            while True:
                current_month_year = self.driver.find_element(By.CSS_SELECTOR, '.DayPicker-Caption').text
                if f"{target_month} {target_year}" in current_month_year:
                    break  # Correct month and year found
                else:
                    # Click next month button to move forward
                    self.click_next_month()
        except Exception as e:
            self.fail(f"An error occurred while selecting the month and year: {str(e)}")

    def click_previous_month(self):
        try:
            previous_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Previous month"]'))
            )
            previous_button.click()
        except Exception as e:
            self.fail(f"An error occurred while clicking the previous month button: {str(e)}")

    def click_next_month(self):
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next month"]'))
            )
            next_button.click()
        except Exception as e:
            self.fail(f"An error occurred while clicking the next month button: {str(e)}")

    def test_flight_booking(self):
        # Input departure and return dates
        departure_date = "Sun Oct 08 2023"
        return_date = "Sun Oct 15 2023"

        # Navigate to the flight booking page
        self.driver.get("https://www.gotogate.com/")

        # Search for a flight with a date range, origin, and destination
        try:
# Select origin from the combo box
            origin_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "searchForm-singleBound-origin-input"))
            )
            origin_input.send_keys("Mumbai")
            time.sleep(3)

            # Wait for the autosuggestion to appear
            origin_suggestion = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "css-1uv24kw"))
            )

            # Find the first list element with the specified class within the autosuggestion
            list_elements = origin_suggestion.find_elements(By.XPATH, ".//*")

            # Ensure that there is at least one list element found
            if list_elements:
                # Find and click the first element within the first list element
                first_list_element = list_elements[0]
                first_element_in_list = WebDriverWait(first_list_element, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//*"))
                )
                first_element_in_list.click()
            else:
                # Handle the case where no list elements with the specified class were found
                raise AssertionError("No elements found with class 'css-1uv24kw' within autosuggestion")

            destination_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "searchForm-singleBound-destination-input"))
            )
            destination_input.send_keys("Bangalore")
            time.sleep(3)

            # Wait for the autosuggestion to appear
            destination_suggestion = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "css-1uv24kw"))
            )

            # Find the first list element with the specified class within the autosuggestion
            list_elements = destination_suggestion.find_elements(By.XPATH, ".//*")

            # Ensure that there is at least one list element found
            if list_elements:
                # Find and click the first element within the first list element
                first_list_element = list_elements[0]
                first_element_in_list = WebDriverWait(first_list_element, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//*"))
                )
                first_element_in_list.click()
            else:
                # Handle the case where no list elements with the specified class were found
                raise AssertionError("No elements found with class 'css-1uv24kw' within autosuggestion")


            # Click the departure date input
            departure_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "singleBound.departureDate"))
            )
            departure_input.click()

            # Select the correct month and year in the date picker
            self.select_month_and_year("October", "2023")

            # Select the departure date based on the input
            if not self.select_date(departure_date):
                raise AssertionError(f"Departure date '{departure_date}' not found in the date picker")

            # Click the return date input
            return_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "singleBound.returnDate"))
            )
            return_input.click()

            # Select the correct month and year in the date picker
            self.select_month_and_year("October", "2023")

            # Select the return date based on the input
            if not self.select_date(return_date):
                raise AssertionError(f"Return date '{return_date}' not found in the date picker")

            # Click the "Search Flights" button
            search_button = WebDriverWait(self.driver, 10).until(
             EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="searchForm-searchFlights-button"]'))
            )
            search_button.click()


            self.take_screenshot("Search_Flight")
            time.sleep(20)  # Adjust the sleep time as needed

        except Exception as e:
            raise AssertionError(f"An error occurred during flight search: {str(e)}")

if __name__ == "__main__":
    unittest.main()
