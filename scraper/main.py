from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

from scraper.utils import get_usage_data

def scrape_usage_data():
  options = webdriver.ChromeOptions()
  options.add_argument("headless")
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  driver.get("https://evergy.com")
  driver.implicitly_wait(10) # seconds

  login_button = driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/div[2]/div[2]/button')
  login_button.click()

  username_field = driver.find_element(By.XPATH, '//*[@id="username"]')
  username_field.send_keys(os.getenv("EVERGY_USERNAME"))

  password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
  password_field.send_keys(os.getenv("EVERGY_PASSWORD"))

  login_form = driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/div[2]/div[2]/div/form')
  login_form.submit()

  cookies = driver.get_cookies()

  print(get_usage_data(driver.get_cookies()))



