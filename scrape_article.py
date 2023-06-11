from newspaper import Article, ArticleException
import csv
import nltk
import sys
sys.path.append('utils')
from clean_data import clean_lines
nltk.download('punkt')

# parse an article with newspaper3k
def get_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article

def scrape_url(url, tag):
    article = get_article(url)
    import re

    pattern = r"\s*\[\s*(edit|\d+)\s*\]\s*"

    article_text = re.sub(pattern, "", article.text)
 
    text_content = str(article_text).split("See alsoReferences")
    scraped_arr = nltk.sent_tokenize(text_content[0].strip())
    # Writing the sentences to a CSV file
    with open(f'fetched_data/{tag}_dataset.csv', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([[clean_lines(value)] for value in scraped_arr])

    return 0

'''if __name__ == "__main__":
    scrape_url("https://en.wikipedia.org/wiki/Brain", "BRAIN")
    scrape_url("https://en.wikipedia.org/wiki/Human_brain", "BRAIN")
'''