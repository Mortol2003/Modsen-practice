from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path 

service = Service(executable_path=binary_path)

driver = webdriver.Chrome(service=service)

driver.get('https://www.example.com')

driver.execute_script("window.localStorage.setItem('myKey', 'myValue');")

value = driver.execute_script("return window.localStorage.getItem('myKey');")
print(f"Value from LocalStorage: {value}")

driver.execute_script("window.localStorage.removeItem('myKey');")

value = driver.execute_script("return window.localStorage.getItem('myKey');")
print(f"Value from LocalStorage after deletion: {value}")

driver.quit()
