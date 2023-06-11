from nltk.stem import PorterStemmer, LancasterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import spacy
import gensim.downloader as api
from generate_embed import which_embedding
import jellyfish

model = api.load("word2vec-google-news-300")

def cosine_sim(x, y):
    similarity_matrix = 0
    x = [word.lower() for word in x if word.lower() in model.key_to_index]
    y = [word.lower() for word in y if word.lower() in model.key_to_index]
    v1 = np.mean([model[word] for word in x], axis=0)
    v2 = np.mean([model[word] for word in y], axis=0)
    if np.isnan(v1).any():
        pass
    else:   
        similarity_matrix = cosine_similarity([v1], [v2])
        similarity_matrix = similarity_matrix[0][0]
    
    return similarity_matrix

def stemming(sentence):
    stemmer = LancasterStemmer()
    stemmed_word = [stemmer.stem(token) for token in sentence]
    # Create a stemmer object
    return stemmed_word

def jaro_winkler(str1, str2):
    # Calculate the Jaro-Winkler distance between two strings
    distance = jellyfish.jaro_winkler(str1, str2)
    return(distance)


#x,y = stemming('Napoleon'), stemming('Napoleonic Wars')
#print (cosine_sim(['Napoleon'], ['Napoleon']))
#print (jaro_winkler('Napoleon', 'Napoleonic Wars'))

