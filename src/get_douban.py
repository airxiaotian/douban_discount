from selenium import webdriver
from selenium.webdriver.common.by import By


def login(username, password):
    driver = webdriver.Chrome(
        './chromedriver/mac-119.0.6045.105/chromedriver-mac-x64/chromedriver')
    driver.get("https://accounts.douban.com/login")
    driver.find_element(By.CLASS_NAME, "account-tab-account").click()
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "account-form-field-submit ").click()
    driver.implicitly_wait(3)
    return driver


def get_group():
    driver.get("https://www.douban.com/group/536786/?ref=sidebar")


driver = login("", "")
driver.get_cookies()
