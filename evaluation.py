import nltk
from nltk.translate.bleu_score import corpus_bleu
#from meteor import Meteor
import numpy as np
#from rouge import Rouge

# Define the actual and generated answers as lists of strings
actual_answer = ['locus coeruleus']
generated_answer = ['Norepinephrine related to Neurotransmitters comes from Locus Coeruleus.']


def bleu(actual_answers, generated_answers):
    # Compute the BLEU Score
    bleu_score = corpus_bleu(actual_answers, generated_answers)
    return bleu_score

def meteor(actual_answer, generated_answer):
    meteor = Meteor()
    score = meteor.compute_score(reference, generated)
    return score


def rouge(actual_answer, generated_answer):
    rouge = Rouge()
    scores = rouge.get_scores(generated, reference)
    return ({'rouge-1': scores[0]['rouge-1']['f'], 'rouge-2': scores[0]['rouge-2']['f'], 'rouge-l': scores[0]['rouge-l']['f']})

print (bleu(actual_answer, generated_answer))