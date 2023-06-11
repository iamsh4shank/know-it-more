import csv
from gensim.models import Word2Vec
import nltk
import numpy as np
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim.downloader as api


def custom_word2vec_model(tag, mode = 'save'):
    if mode == 'save':
        # Save the model
        csv_file_path = f'fetched_data/{tag}_dataset.csv'
        # Read data from CSV file
        sentences = []
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                sentences.append(row[0])

        # Preprocess the sentences
        processed_sentences = [nltk.word_tokenize(sentence.lower()) for sentence in sentences]
        model = Word2Vec(processed_sentences, window=5, min_count=1, workers=4)
        model.wv.save_word2vec_format(f'embed_models/{tag}_word2vec.txt')
    else:
        model = KeyedVectors.load_word2vec_format(f'embed_models/{tag}_word2vec.txt')
        return model

def tf_idf():
    return TfidfVectorizer()

def word2vec_model():
    model = api.load("word2vec-google-news-300")
    return model
