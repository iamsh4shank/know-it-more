import os
import nltk
nltk.download('punkt')
import csv
from utils.clean_data import clean_lines

def read_file(file_path, tag):
    with open(f'{file_path}', 'r') as f:
        file_contents = f.read()
        file_data = nltk.sent_tokenize(file_contents)

    # Writing the sentences to a CSV file
    with open(f'fetched_data/{tag}_dataset.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([[clean_lines(f'{value}')] for value in file_data])

    return 0

if __name__ == '__main__':
    read_file(file_path = 'dataset/text_data/text_data/Otter.txt', tag = 'OTTER')