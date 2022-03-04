from selenium.webdriver import Firefox  # I used Firefox as my webdriver. You have to have Firefox on you machine.
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import json

# To download geckodriver visit https://github.com/mozilla/geckodriver/releases down to "Assets" part
# and download right version for your machine.

# Down here you have to put full PATH to your geckodriver
service = Service(r'%FULL PATH TO GECKODRIVER%')
options = Options()
options.binary_location = r'%FULL PATH TO FIREFOX%'

tracking_id = input('Enter your tracking ID\n')
driver = Firefox(service=service, options=options)
driver.get('https://parcelsapp.com/widget')

search = driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/input[@placeholder="Enter tracking number"]')
driver.implicitly_wait(10)
search.send_keys(tracking_id)  # putting tracking ID

button = driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/button')
button.click()  # clicking a button
driver.implicitly_wait(10)

#  Adding data to dictionary by every event.
#  Key is tracking date + time and values are all content.
data = {}

events = driver.find_elements(by=By.CLASS_NAME, value='event')
for event in events:
    event_data = {
        'track_date': event.find_element(by=By.CLASS_NAME, value='track-content-date').text,
        'track_time': event.find_element(by=By.CLASS_NAME, value='track-content-time').text,
        'track_status': event.find_element(by=By.CLASS_NAME, value='track-content-status').text
    }

    data[f"{event.find_element(by=By.CLASS_NAME, value='track-content-date').text}_{event.find_element(by=By.CLASS_NAME, value='track-content-time').text}"] = event_data

#  At last, writing the json file
json_object = json.dumps(data, indent=4)
with open(f"{tracking_id}.json", "w") as outfile:
    outfile.write(json_object)

driver.close()

print(input('Press enter to continue...\n'))
