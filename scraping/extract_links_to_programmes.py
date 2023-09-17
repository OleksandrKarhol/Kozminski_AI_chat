import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("Kozminski_AI_chat/scraping/html/main_page.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

elements = {
    'menu_button' : '//*[@id="block-headerblock"]/div[1]/div[1]/div/div/div/div[1]/div[2]/a', 
    'menu_items' : []
}
a = 1
for link_button in soup.find_all('a'):
    if link_button.has_attr('class'):
        if link_button['class'] == ['menu-item']:
            elements['menu_items'].append({f'{a}': f'{link_button.string}'})
            a +=1

# Finding the structure of the website 
#Initializing webderiver
_DRIVER_FILEPATH = '...'
_PROFILE_PATH = '...'
_URL = 'https://www.kozminski.edu.pl/en'

def set_driver(_driver_path, _profile, _desired_capabilities, _options):
    driver = webdriver.Firefox(executable_path=_driver_path,
                                firefox_profile=_profile,
                                desired_capabilities=_desired_capabilities,
                                options=_options)
    return driver

def set_window_action(_webpage, _driver):
    _driver.get(_webpage)
    _driver.switch_to.window(_driver.current_window_handle)

    action = ActionChains(_driver)
    return action

profile = webdriver.FirefoxProfile(_PROFILE_PATH)
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX
opts = webdriver.FirefoxOptions()
opts.headless = False
opts.binary_location = '...'

driver = set_driver(_driver_path=_DRIVER_FILEPATH, _profile=profile,
                                    _desired_capabilities=desired, _options=opts)

_action = set_window_action(_webpage=_URL, _driver=driver)

a = 1
for element in elements['menu_items']: 
    time.sleep(5)
    _action.move_to_element(driver.find_element(by=By.XPATH, value= elements['menu_button'])).click().perform()

    try: 
        time.sleep(4)
        print(element[f'{a}'], type(element[f'{a}']))
        link_element = driver.find_element(By.LINK_TEXT, element[f'{a}'].upper())
        print(link_element.text)
        link_element.click()
    except: 
        link_element = driver.find_element(By.LINK_TEXT, element[f'{a}'])
        print(link_element.text)
        link_element.click()


    time.sleep(5)
    driver.back()
    a += 1