import time
from selenium.webdriver.common.by import By

from selenium import webdriver
browser = webdriver.Chrome(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
browser.maximize_window()
browser.get("https://qzone.qq.com/")
time.sleep(1.2)
browser.switch_to.frame('login_frame')
browser.find_element(By.ID,'switcher_plogin').click()
time.sleep(1)
browser.find_element(By.ID,'u').send_keys("usern@ame")
browser.find_element(By.ID,'p').send_keys("p@ssw0rd")
time.sleep(1)
browser.find_element(By.ID,'login_button').click()
time.sleep(10)
cookies_list = browser.get_cookies()
for cookie in cookies_list:
    if 'name' in cookie and 'value' in cookie:
        print(cookie['name']+"|"+cookie['value'])