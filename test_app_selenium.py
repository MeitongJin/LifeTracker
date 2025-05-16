import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

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

    def click_next(self):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        next_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]'))
        )
        next_button.click()

    # 1. Test the registration process
    def test_1_register_new_user(self):
        driver = self.driver
        driver.get(f"{self.base_url}/register")
        driver.find_element(By.NAME, "firstname").send_keys("Selenium")
        driver.find_element(By.NAME, "lastname").send_keys("Test")
        unique_email = f"test{int(datetime.now().timestamp())}@example.com"
        driver.find_element(By.NAME, "email").send_keys(unique_email)
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
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign Out"))
        ).click()
        WebDriverWait(driver, 5).until(EC.url_contains("/login"))
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

    # 5. Test accessing home page after login
    def test_7_home_access_after_login(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        driver.find_element(By.NAME, "email").send_keys("testselenium@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.TAG_NAME, "form").submit()

        WebDriverWait(driver, 5).until(EC.url_contains("/home"))
        self.assertIn("/home", driver.current_url)

        self.assertIn("Selenium", driver.page_source)



if __name__ == '__main__':
    unittest.main()
