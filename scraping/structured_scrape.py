import csv
import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    response = requests.get(url)
    return response.content

def extract_heading_and_paragraphs(soup):
    data = []

    first_element = soup.h1
    for header in first_element.find_all_next('h2'):
        header_name = header.string
        for paragraph in header.find_all_next('p'):
            para_text = paragraph.string
            if para_text and header_name:
                data.append([f"Header : {header_name}", f"Text: {para_text}"])

    for i in range(len(data)):
        for j in range(len(data)):
            if data[-i][1] == data[j][1]: continue
            if data[-i][1] in data[j][1]:
                data[j][1] = str(data[j][1]).replace(str(data[-i][1]), '')
    
    return data

def extract_tables(soup):
    data = []
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        table_data = []
        for row in rows:
            cells = [cell.get_text().strip() for cell in row.find_all(['th', 'td'])]
            table_data.append(cells)
        data.append(table_data)
    return data

def extract_links(soup):
    data = []
    all_links = soup.find_all('a')
    for link in all_links:
        href = link.get('href')
        text = link.string
        if href and text:
            data.append([f' Link: {href}', f'Text: {text}'])
    return data

def extract_lists(soup):
    data = []
    list_items = soup.find_all(['ul', 'ol'])
    for lst in list_items:
        list_data = [item.get_text().strip() + '\n' for item in lst.find_all('li')]
        data.append(list_data)
    return data

def save_to_txt(data, filename):
    print(data)
    with open(filename, 'a') as file:
        for line in data:
            file.write(str(line) + '\n')

def save_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def delete_header_footer(soup):
    header_elements = soup.find_all('header')
    footer_elements = soup.find_all('footer')

    for element in header_elements:
        element.extract()

    for element in footer_elements:
        element.extract()

def main(url):
    content = get_page_content(url)
    soup = BeautifulSoup(content, 'html.parser')

    # Remove header and footer elements from the soup
    delete_header_footer(soup)

    # Extract headings and paragraphs
    heading_paragraph_data = extract_heading_and_paragraphs(soup)
    save_to_csv(heading_paragraph_data, 'data.csv')

    # Extract tables
    table_data = extract_tables(soup)
    save_to_csv(table_data, 'data.csv')

    # Extract links
    links = extract_links(soup)
    save_to_csv(links, 'data.csv')

    # Extract lists
    list_data = extract_lists(soup)
    save_to_csv(list_data, 'data.csv')

if __name__ == "__main__":
    main('https://www.kozminski.edu.pl/en/programs/undergraduate-programs-bachelor/bachelor-management')
