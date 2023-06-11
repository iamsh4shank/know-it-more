import csv
import requests
import nltk
from bs4 import BeautifulSoup

from utils.clean_data import clean_lines
nltk.download('punkt')

def scrape_url(url, tag):
    """Function to scrape data from the URL

    Args:
        url (_type_): string
        tag (_type_): string

    Example:
        fetch_url(url = 'https://en.wikipedia.org/wiki/Web_scraping', tag = 'web_scraping')
    """

    # Fetching the content of the URL and converting it into a BeautifulSoup object
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', {'id': 'mw-content-text'})

    # Removing unwanted sections and headings
    content_div = soup.find('div', {'class': 'mw-parser-output'})
    see_also = content_div.find('div', {'class': 'div-col'})
    references = soup.find('div', {'class': 'reflist'})
    table = soup.find('table', {'class': 'box-Update plainlinks metadata ambox ambox-content ambox-Update'})
    sup_script = content_div.find('sup', {'class': 'reference'})
    notes = soup.find('div', {'class': 'reflist reflist-lower-alpha'})
    citations = soup.find('div', {'class': 'reflist reflist-columns references-column-width'})
    extra_ref = soup.find('div', {'class': 'refbegin'})
    for heading in content_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        heading.decompose()

    if see_also:
        see_also.decompose()

    if references:
        references.decompose()
    
    if table:
        table.decompose()
    
    if sup_script:
        sup_script.decompose()
    
    if notes:
        notes.decompose()
    
    if citations:
        citations.decompose()

    if extra_ref:
        extra_ref.decompose()
    # Extracting the text content and tokenizing it
    text_content = content.text.strip()
    scraped_arr = nltk.sent_tokenize(text_content)

    # Writing the sentences to a CSV file
    with open(f'fetched_data/{tag}_dataset.csv', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([[clean_lines(value)] for value in scraped_arr[:-1]])

    return 0

if __name__ == '__main__':
    scrape_url(url = 'https://en.wikipedia.org/wiki/Napoleon', tag = 'TEST')