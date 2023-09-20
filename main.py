import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from test import test_booking, test_login

# Initialize the Chrome WebDriver using webdriver-manager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

if __name__ == "__main__":
    # Initialize test suites for each module
    booking_test_suite = unittest.TestLoader().loadTestsFromModule(test_booking)
    login_test_suite = unittest.TestLoader().loadTestsFromModule(test_login)

    # Combine the test suites into a single test suite
    test_suite = unittest.TestSuite([ booking_test_suite])

    # Initialize test runner
    test_runner = unittest.TextTestRunner()

    # Run the test suite
    result = test_runner.run(test_suite)

    # Clean up resources
    driver.quit()

    # Print test results
    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print("Some tests failed.")
