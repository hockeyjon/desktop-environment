from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# create a new Firefox session
driver = webdriver.Firefox()
driver.maximize_window()

# navigate to the application home page
driver.get("https://mint.intuit.com/login.event?task=L&messageId=6&country=US&nextPage=overview.event")
time.sleep(15)

field = driver.find_element_by_id("ius-userid")
field.clear()
field.send_keys("jonathan.kopp@gmail.com")
field = driver.find_element_by_id("ius-password")
field.clear()
field.send_keys("gunther13")
driver.find_element_by_id("ius-sign-in-submit-btn").click()
time.sleep(10)
driver.find_element_by_link_text("Transactions").click()
time.sleep(2)
driver.find_element_by_id("sort-cash").click()
time.sleep(2)
driver.find_element_by_id("controls-add").click()
time.sleep(2)
field = driver.find_element_by_id("txnEdit-date-input")
field.clear()
field.send_keys("Mar 16")
#time.sleep(2)
field = driver.find_element_by_id("txnEdit-merchant_input")
field.clear()
field.send_keys("Test Description")
field = driver.find_element_by_id("txnEdit-category_input")
field.clear()
field.send_keys("Uncategorized")
#time.sleep(2)
field = driver.find_element_by_id("txnEdit-amount_input")
field.clear()
field.send_keys("2.34")
driver.find_element_by_id("txnEdit-submit").click()
driver.quit()
print "Import complete."

