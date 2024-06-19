# This code tests whether user is able to add URL to the Knowledge Base
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time

app_URL = "http://localhost:8501/"
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
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
