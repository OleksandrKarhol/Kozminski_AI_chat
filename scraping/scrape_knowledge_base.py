from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from scrape_text import get_scraped_text
import pandas as pd 
import time
import json

SOURCE = 'https://kozminski.my.site.com/s/knowledge-base'
DRIVER = webdriver.Firefox()

def saveJson(name, data):

    with open(name, "w") as json_file:
        json.dump(data, json_file, indent=4)
            

def get_page_content(url, sleepTime = 10):
    DRIVER.get(url)
    time.sleep(sleepTime)
    page_source = DRIVER.page_source
    return page_source

def get_category_names(soup) -> dict:
    global SUBJECTS
    SUBJECTS = {}
    all_subjects = soup.find_all('span')
    for subject in all_subjects:
        subject_name = subject.string
        subject_link = subject.parent.get('href')
        if subject_link != None and subject_name != None:
            SUBJECTS[f'{subject_name}'] = subject_link

def get_article_names(soup, subject):

    articles = {}
    all_articles = soup.find_all('h2')
    for article in all_articles:
        article_name = article.string
        article_link = article.parent.get('href')
        if article_link != None and article_name != None:
            article_link = 'https://kozminski.my.site.com' + article_link
            article_content = get_scraped_text(DRIVER, article_link, subject, article_name.replace(' ', '_'))
            articles[f'{article_name}'] = article_content

    SUBJECTS[f'{subject}'] = articles    

def get_page_structure():
    content = get_page_content(SOURCE, 10)
    soup = BeautifulSoup(content, 'html.parser')
    get_category_names(soup)
    for subject in SUBJECTS:
        url = SUBJECTS[subject]
        content = get_page_content(url, 0)
        soup = BeautifulSoup(content, 'html.parser')
        get_article_names(soup, subject)
        saveJson("scraping_map.json", SUBJECTS)
     
def save_scraped_text():
    for category in SUBJECTS:
        article_names = SUBJECTS[category]
        for name in article_names:
            article_link = article_names[name]
            article_content = get_scraped_text(article_link)
            article_names[name] = article_content
    
if __name__ == '__main__':  
    get_page_structure()
    save_scraped_text()