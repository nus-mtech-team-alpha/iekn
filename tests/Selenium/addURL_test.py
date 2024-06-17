# This code tests whether user is able to add URL to the Knowledge Base
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

app_URL = "http://localhost:8502/"
test_URL = "https://www.channelnewsasia.com/singapore/singapore-budget-2024-lawrence-wong-live-blog-4122681"
screenshot_path = "/home/hizam/Desktop/addURL_screenshot.png"

class AddURL(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_add_u_r_l(self):
        driver = self.driver
        driver.get(app_URL)
        driver.find_element(By.XPATH, "//div[@id='root']/div/div/div/div/div/section[2]").click()
        driver.find_element(By.ID, "text_input_1").click()
        driver.find_element(By.ID, "text_input_1").clear()
        driver.find_element(By.ID, "text_input_1").send_keys(test_URL)
        driver.find_element(By.XPATH, "//div[@id='root']/div/div/div/div/div/section/div/div[2]/div/div/div/div/div[2]/div/button/div/p").click()
        driver.find_element(By.XPATH, "//textarea[@name='']").click()

        # Take a screenshot
        time.sleep(5)
        driver.save_screenshot(screenshot_path)
        driver.quit()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
