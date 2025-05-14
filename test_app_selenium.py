import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

class LifeTrackerSeleniumTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)
        cls.base_url = "http://127.0.0.1:5000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # 1. Test the registration process
    def test_1_register_new_user(self):
        driver = self.driver
        driver.get(f"{self.base_url}/register")
        driver.find_element(By.NAME, "firstname").send_keys("Selenium")
        driver.find_element(By.NAME, "lastname").send_keys("Test")
        driver.find_element(By.NAME, "email").send_keys("testselenium@example.com")
        driver.find_element(By.NAME, "phone").send_keys("1234567890")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "password_confirm").send_keys("password123")
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(2)
        self.assertIn("login", driver.current_url)

    # 2. Test the login successfully
    def test_2_login_success(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login")
        driver.find_element(By.NAME, "email").send_keys("testselenium@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(2)
        self.assertIn("home", driver.current_url)

    # 3. Test the logout process
    def test_3_logout(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)
        self.assertIn("login", driver.current_url)

    # 4. Test the login failure
    def test_4_login_fail(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("wrong@example.com")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("wrongpass")
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)
        self.assertIn("Invalid email or password", driver.page_source)

    # 5. Test the protected page redirect
    def test_5_protected_page_redirect(self):
        driver = self.driver
        driver.get(f"{self.base_url}/daily_input")
        time.sleep(1)
        self.assertIn("login", driver.current_url)

    # 6. Test the daily input form submission
    def test_6_fill_and_submit_daily_input_form(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        # login
        driver.find_element(By.NAME, "email").send_keys("testselenium@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(2)

        # navigate to daily input page
        driver.get(f"{self.base_url}/daily_input")
        time.sleep(1)

        # fill out the form
        driver.find_element(By.XPATH, '//input[@name="exercise" and @value="yes"]').click()
        time.sleep(0.5)
        driver.find_element(By.ID, "exercise_hours").send_keys("1.5")
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        driver.find_element(By.ID, "water_intake").send_keys("2.0")
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        driver.find_element(By.ID, "sleep_hours").send_keys("7.5")
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        driver.find_element(By.ID, "reading_hours").send_keys("1.2")
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        driver.find_element(By.ID, "meals").send_keys("3")
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        driver.find_element(By.ID, "screen_hours").send_keys("4.5")
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        Select(driver.find_element(By.ID, "productivity")).select_by_visible_text("8")
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        driver.find_element(By.XPATH, '//input[@name="mood" and @value="happy"]').click()
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        driver.find_element(By.ID, "agreeCheck").click() # Simulated click to check the agree box
        driver.find_element(By.ID, "submitBtn").click()
        time.sleep(3)

        self.assertIn("/daily_output", driver.current_url)

if __name__ == '__main__':
    unittest.main()
