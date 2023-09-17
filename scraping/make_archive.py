from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd

# Set up the Chrome WebDriver (Make sure you have chromedriver installed and in PATH)
driver = webdriver.Firefox()

def extract_links(_url, _driver):

    _driver.get(_url)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    # Remove header and footer elements from the soup
    header_elements = soup.find_all('header')
    footer_elements = soup.find_all('footer')

    for element in header_elements:
        element.extract()

    for element in footer_elements:
        element.extract()

    # get all links 
    all_links = soup.find_all('a')

    programme_links = []
    for link in all_links:
        href = link.get('href')
        text = link.string
        if href and text != None and 'kozminski' in str(href).lower():
            programme_links.append(href)
    
    return programme_links

def append_to_file(file_path, lines_to_append):
    with open(file_path, 'a') as file:
        file.write(lines_to_append + '\n')

def close_popup(_driver):

    wait = WebDriverWait(_driver, 30)
    wait.until(EC.presence_of_element_located((By.ID, '/html/body/div[2]/div/div/div[2]/button[1]')))

    accept_cookies_button = _driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/button[1]')
    accept_cookies_button.click()

def save_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def extract_text(_url, _driver):
    
    _driver.get(_url)
    #close_popup(_driver)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    # get a clean title
    titles = soup.find_all('title')
    
    title = titles[0]
    title = title.string
    if '- Kozminski University - Warsaw, Poland' in title:
        title.replace('- Kozminski University - Warsaw, Poland', '')
    
    # Remove header and footer elements from the soup
    header_elements = soup.find_all('header')
    footer_elements = soup.find_all('footer')

    for element in header_elements:
        element.extract()

    for element in footer_elements:
        element.extract()

    #save file and title
    directory = '/Users/apple/Desktop/chat_project/scraping/archive_big/'
    #append_to_file(directory + f'{title}.txt', title)
    
    # save all text to the same file
    all_text = soup.get_text()
    #append_to_file(directory + f'{title}.txt', all_text)
    TITLES.append(title)
    ALL_TEXT.append(all_text)
    

TITLES = []
ALL_TEXT = []
list_of_links = extract_links('https://www.kozminski.edu.pl/en/programs', driver)
print("links found: ", len(list_of_links))
for link in list_of_links:
    extract_text(link, driver)

DF = pd.DataFrame(list(zip(TITLES, ALL_TEXT)), columns = ['Page_title', 'Page_content'])
DF.to_csv("data.csv")