# This code tests whether user is able to upload PDF to the Knowledge Base
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time

app_URL = "http://localhost:8501/"
upload_path = "/home/hizam/Desktop/text_file.pdf"
screenshot_path = "/home/hizam/Desktop/addFile_screenshot.png"

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        driver = self.driver
        driver.get(app_URL)
        driver.find_element(By.XPATH, "//div[@id='root']/div/div/div/div/div/section/div/div[2]/div/div/div/div/div[3]/div/section/button").click()
        driver.find_element(By.XPATH, "//input[@type='file']").clear()
        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(upload_path)
        driver.find_element(By.XPATH, "//textarea[@name='']").click()

        # Take a screenshot
        time.sleep(5)
        driver.save_screenshot(screenshot_path)
        driver.quit()
    
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
