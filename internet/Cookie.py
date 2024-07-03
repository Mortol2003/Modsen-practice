from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path 

service = Service(executable_path=binary_path)

driver = webdriver.Chrome(service=service)

driver.get('https://www.example.com')

driver.add_cookie({'name': 'myCookie', 'value': 'myValue'})

cookie = driver.get_cookie('myCookie')
print(f"Value from Cookie: {cookie['value']}")

driver.delete_cookie('myCookie')

cookie = driver.get_cookie('myCookie')
print(f"Value from Cookie after deletion: {cookie}")

driver.quit()
