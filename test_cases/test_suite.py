import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import random
from webdriver_manager.chrome import ChromeDriverManager

class HomeTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # options.add_argument('headless')
        cls.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        cls.base_url = "http://127.0.0.1:5000/"

    def test_home(self):
        self.driver.get(self.base_url )
        WebDriverWait(self.driver, 15).until(expected_conditions.title_is('YoungWonks Open Source Summer Project 2021'))
        self.assertIn('Hello, world!', self.driver.page_source)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()