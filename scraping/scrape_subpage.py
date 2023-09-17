import requests
from bs4 import BeautifulSoup
import time
import sys 

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Initializing webderiver
_DRIVER_FILEPATH = '...'
_PROFILE_PATH = '...'
_URL = 'https://www.kozminski.edu.pl/en/programs/undergraduate-programs-bachelor/bachelor-management'

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
opts.binary_location = '/Applications/Firefox.app/Contents/MacOS/firefox'

#driver = set_driver(_driver_path=_DRIVER_FILEPATH, _profile=profile,
#                                   _desired_capabilities=desired, _options=opts)
#
#_action = set_window_action(_webpage=_URL, _driver=driver)

"""
tags = []
for tag in soup.find_all(True):
    tags.append(tag.name)

tags = list(set(tags))
print('tags: ', tags, len(tags))

links = []
for link in soup.find_all('a'):
    links.append({f'{link.get("href")}' : f'{link.string}'})
    print({f'{link.get("href")}' : f'{link.string}'})

#print('links: ', links, len(links))

# buttons with links 
# buttons with functions (href) 
buttons = []

headers = []

patagraphs = []

strongs = []
for strong in soup.find_all('strong'):
    print('strong :', strong.string)
    for desc in  strong.descendants:
        if desc != strong.string:
            print('desc: ', desc.string)
    strongs.append({f'{strong}' : f'{strong.string}'})
    #print({f'{strong}' : f'{strong.string}'})

for string in soup.strings:
    if string != None and string != '\n':
        print('string: ', string)
        print(soup.find_all(True, text = string)[0].name)
"""


"""

# Body childre approach: find children of a body element to understand a basic structure. 
def minimum_element(element):
    # find the minimum child 
    if list(element.findChildren()):
        for element_child in list(element.findChildren()):
            if element_child.string != None and element_child.string != '\n':
                #print(element.string, element.name)
                minimum_element(element_child)
                #print(i)
                i +=1
    else:
        if element.name in "div, strong, p, h1, h1, h3, span, ":
            print("minimum_element: ", str(element.string), str(element.name))

# Find the <body> tag
body_tag = soup.body

# Find all the children of the <body> tag
children = list(body_tag.findChildren())
print(len(children))

for body_child in children[:4]:
    if body_child != None and body_child != '\n':
        minimum_element(body_child)
"""




# interest: <body> --> <main> --> <h> and <p> + add list + add tables
# skip: script, footer, 

# Beautiful soup
with open("Kozminski_AI_chat/scraping/html/sub-page.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

def get_attribute(element, attribute = None):
    if attribute == 'string':
        return str(element.string)
    elif attribute == 'tag':
        return str(element.name)
    elif attribute == 'class':
        return str(element.get['class'])
    elif attribute == 'parent' or attribute == None:
        return element
    else:
        print('unknown attribute')
    
def get_parent_attribute(element, attribute:str = None):
    parent = element.parent
    return get_attribute(parent, attribute)
    
def get_descendant_attribute(element, attribute:str = None):
    descendant = element.descendants
    return get_attribute(descendant, attribute)

def get_children_attribute(element, attribute:str = None):
    child = element.findChildren()
    return get_attribute(child, attribute)

def extract_lists(element = None):
    list_dict = {}
    if element:
        element.find_all('ul')
    else:
        lists = soup.find_all('ul')
    i = 1
    for list in lists:
        list_dict[f'list_{i}'] = []
        
        list_elements = list.findChildren()
        for element in list_elements:
            
            if element != None and element != "\n" and "li" in str(element):
                list_dict[f'list_{i}'].append(element)
        i += 1
    return list_dict

def find_base_case(element, data_storage: list):
    
    try:
        list_of_children = list(element.children)

        list_of_children = [x for x in list_of_children if x != None and x != '\n']
        if list_of_children:
            for element_child in list_of_children:
                if element_child != None and element_child != '\n':
                    find_base_case(element_child, data_storage)
        return data_storage
    except AttributeError: 
        data_storage.append(element)
        return data_storage



#def find_family(base_case):
    # look for siblings
    # if none --> search parents --> if string == none
    # search parents until string is found
    # when parents found --> search parent's siblings
    # when parents siblings found --> search their children 



def get_link_string(link, data_storage):
    BASE_CASES = []
    base_cases = find_base_case(link, data_storage = data_storage)
    link_string = ''
    for base_case in base_cases:
        link_string += ' ' + get_attribute(base_case, 'string')
    
    
    return link_string


#for link in soup.findAll('a', class_ = 'test'):
    #print(get_link_string(link))

with open('text_data.txt', 'a') as f:
    for string in soup.strings:
        if string != None and string != '\n':
            f.write(f'{string}')




h_3 = []
h_2 = []
h_1 = []
p = []

"""
lists = extract_lists()
for i in range(len(lists)):
    print('list', lists[f"list_{i+1}"])
"""


"""
first_element = soup.h1
for header_2 in first_element.find_all_next('h2'):
    print("header 2: ", header_2.string)
    for header_3 in first_element.find_all_next('h3'):
        print("header 3: ", header_3.string)
        for paragraph in header_3.find_all_next('p'):
            
            if paragraph.string != None and paragraph.string != "\n" and paragraph.string not in p:
                p.append(paragraph.string)
                print("paragraph: ", paragraph.string)
        for span in header_3.find_all_next('span'):
            
            if span.string != None and span.string != "\n" and span.string not in p:
                p.append(span.string)
                print("span: ", span.string)
        
"""

# flatten the .html code and transform all string tags into <h> or <p> + delete all divs 
# delete all elements without strings and flatten