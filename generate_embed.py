import spacy
import numpy as np
import pickle
import nltk

from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
from gen_embed_model import custom_word2vec_model, tf_idf, word2vec_model

def which_embedding(tag = None, model_type = 'spacy'):
    """Set model type

    Args:
        tag (_type_, optional): Tag name string Defaults to None.
        model_type (str, optional): embedding type. Defaults to 'spacy'.

    Raises:
        ValueError: Type is not what required

    Returns:
        _type_: _description_
    """
    if model_type == 'spacy':
        model = spacy.load('en_core_web_md')
        return model
    elif model_type == 'c_word2vec':
        return custom_word2vec_model(tag, mode = 'load')
    elif model_type == "word2vec":
        return word2vec_model()
    elif model_type == 'tfidf':
        return tf_idf()
    else:
        raise ValueError('type must be either "spacy" or "word2vec"')

def gen_embed(sentence, type_embed = 'spacy', tag = None):
    if type_embed == 'spacy':
        spacy_model = which_embedding(model_type = 'spacy')
        tokens = [token for token in spacy_model(sentence) if not token.is_stop]
        if tokens:
            embedding = np.mean([token.vector for token in tokens], axis=0)
        else:
            embedding = np.zeros((nlp.vocab.vectors.shape[1],))
        return embedding
    elif type_embed == 'c_word2vec':
        word_emb_model = which_embedding(model_type = 'c_word2vec', tag = "TEST")
        word_vectors = np.mean([word_emb_model[word] for word in sentence if word in word_emb_model.key_to_index], axis=0)
        return word_vectors
    elif type_embed == 'tfidf':
        vectorizer = which_embedding(model_type = 'tfidf')
        vectorized_sentence = vectorizer.fit_transform([sentence])
        return vectorized_sentence

    elif type_embed == 'word2vec':
        word2vec_model = which_embedding(model_type = 'word2vec')
        embed = np.mean([word2vec_model[word] for word in sentence if word in word2vec_model.key_to_index], axis=0)
        return embed

def rank_corpus(query, context, embed_type = 'spacy'):
    context_arr = nltk.sent_tokenize(context)
    if embed_type == 'spacy':
        query_embedding = gen_embed(query, type_embed = 'spacy')
        context_embedding = []
        for context in context_arr:
            context_embedding.append(gen_embed(context, type_embed = 'spacy'))
    elif embed_type == 'c_word2vec':
        query_embedding = gen_embed(query, type_embed = 'c_word2vec', tag='TEST')
        context_embedding = []
        for context in context_arr:
            context_embedding.append(gen_embed(context, type_embed = 'c_word2vec', tag='TEST'))
    elif embed_type == 'word2vec':
        query_embedding = gen_embed(query, type_embed = 'word2vec')
        context_embedding = []
        for context in context_arr:
            context_embedding.append(gen_embed(context, type_embed = 'word2vec'))
    elif embed_type == 'tfidf':
        query_embedding = gen_embed(query, type_embed = 'tfidf')
        context_embedding = []
        for context in context_arr:
            context_embedding.append(gen_embed(context, type_embed = 'tfidf'))
    # Compute the cosine similarity between the query and each sentence in the corpus
    similarities = []
    for sentence_embedding in context_embedding:
        if embed_type == 'tfidf':
            query_embedding = np.array(query_embedding.toarray()[0])
            sentence_embedding = np.array(sentence_embedding.toarray()[0])

        similarity = np.dot(query_embedding, sentence_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(sentence_embedding))
        similarities.append(similarity)

    # Rank the sentences based on cosine similarity
    ranked_sentences = sorted([(i, sentence, similarity) for i, (sentence, similarity) in enumerate(zip(context_arr, similarities))], key=lambda x: x[2], reverse=True)

    ranked_doc = {}
    # Print the top 10 ranked sentences
    for i, sentence, similarity in ranked_sentences[:2]:
        ranked_doc[i] = {"Similarity score": similarity, "Sentence": sentence}
        #print(f"Similarity score: {similarity} Sentence: {sentence}")

    return ranked_doc



if __name__ == '__main__':
    query = "How was Napoleon related to French Revolution and France?"
    context = "Napoleon (1769-1821) was a military and political leader of France who rose to prominence during the French Revolution and became the emperor of France from 1804 to 1814. Napoleon Bonaparte played a significant role in the French Revolution. He was born in Corsica in 1769, and after studying at a military academy in France, he quickly rose through the ranks of the French military. In 1799, Napoleon seized power in a coup and became the First Consul of France, effectively making him the leader of the country.  The revolution began with the storming of the Bastille, a symbol of royal tyranny, and the establishment of the National Assembly, which aimed to create a constitutional monarchy. It was characterized by a series of radical changes that abolished the monarchy, overthrew the aristocracy, and established the First French Republic."
    #print (rank_corpus(query, context, 'spacy'))
    #print (rank_corpus(query, context, 'c_word2vec'))
    #print (rank_corpus(query, context, 'word2vec'))
    print (rank_corpus(query, context, 'tfidf'))




    
