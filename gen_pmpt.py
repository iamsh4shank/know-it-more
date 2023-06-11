import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from generate_embed import rank_corpus
import random
import numpy as np
import nltk

nltk.download("punkt",  quiet=True)
nltk.download("brown",  quiet=True)
nltk.download("wordnet",  quiet=True)
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize
import nltk

nltk.download("stopwords",  quiet=True)
from nltk.corpus import stopwords
import string
import pke
import traceback
from flashtext import KeywordProcessor
from generate_kg import load_kg
from stemming import stemming, cosine_sim, jaro_winkler
#m preprocess_nodes import preprocessed_node
from gen_sentence import gen_sen

def load_model(model="ramsrigouthamg/t5_squad_v1"):
    question_model = T5ForConditionalGeneration.from_pretrained(
        "ramsrigouthamg/t5_squad_v1"
    )
    question_tokenizer = T5Tokenizer.from_pretrained("ramsrigouthamg/t5_squad_v1")
    return question_model, question_tokenizer


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


set_seed(42)


def postprocesstext(content):
    final = ""
    for sent in sent_tokenize(content):
        sent = sent.capitalize()
        final = final + " " + sent
    return final


def get_nouns_multipartite(content):
    out = []
    try:
        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(input=content)
        #    not contain punctuation marks or stopwords as candidates.
        pos = {"PROPN", "NOUN"}
        # pos = {'PROPN','NOUN'}
        stoplist = list(string.punctuation)
        stoplist += ["-lrb-", "-rrb-", "-lcb-", "-rcb-", "-lsb-", "-rsb-"]
        stoplist += pke.lang.stopwords.get("en")
        extractor.candidate_selection(pos=pos)
        # 4. build the Multipartite graph and rank candidates using random walk,
        #    alpha controls the weight adjustment mechanism, see TopicRank for
        #    threshold/method parameters.
        extractor.candidate_weighting(alpha=1.1, threshold=0.75, method="average")
        keyphrases = extractor.get_n_best(n=15)

        for val in keyphrases:
            out.append(val[0])
    except:
        out = []
        traceback.print_exc()

    return out


def get_keywords(originaltext, num_prompt = 5):
    keywords = get_nouns_multipartite(originaltext)
    keyword_processor = KeywordProcessor()
    for keyword in keywords:
        keyword_processor.add_keyword(keyword)

    keywords_found = keyword_processor.extract_keywords(originaltext)
    keywords_found = list(set(keywords_found))
    important_keywords = []
    for keyword in keywords:
        if keyword in keywords_found:
            important_keywords.append(keyword)

    return important_keywords[:num_prompt]


def get_question(context, answer, model, tokenizer):
    text = "context: {} answer: {}".format(context, answer)
    encoding = tokenizer.encode_plus(
        text,
        max_length=384,
        pad_to_max_length=False,
        truncation=True,
        return_tensors="pt",
    )
    input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

    outs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        early_stopping=True,
        num_beams=5,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        max_length=72,
    )

    dec = [tokenizer.decode(ids, skip_special_tokens=True) for ids in outs]

    Question = dec[0].replace("question:", "")
    Question = Question.strip()
    return Question


def gen_text(ranked_doc):
    doc = []
    for d in ranked_doc.values():
        doc.append(d["Sentence"])

    text = " ".join(doc)
    text = postprocesstext(text)
    text = text.strip()

    return text

def gen_final_info(query, context, embed_type = 'spacy', num_prompt = 5, tag = 'TEST'):
    ranked_doc = rank_corpus(query, context, embed_type)
    text = gen_text(ranked_doc)
    imp_keywords = get_keywords(query, num_prompt)
    query_tokens = []
    prompt = []
    print (imp_keywords)
    model, tokenizer = load_model()
    for key in imp_keywords:
        ques = get_question(text, key, model, tokenizer)
        prompt.append(ques)
        query_tokens.append(key.capitalize())
    
    kg = load_kg(f'gen_KG/{tag}.pkl')
    pm_tags = {}
    query_tokens = [x.lower() for x in query_tokens]
    pm = kg.query(query_tokens)
    new_tags = []
    possible_nodes = kg.get_entities()

    query_set = set(query_tokens)
    print ('working till here')
    for extra_node in possible_nodes:
        if extra_node.lower() not in query_set and any(jaro_winkler(extra_node.lower(), avail_node.lower()) > 0.8 for avail_node in query_set):
            new_tags.append(extra_node.lower())
    print ('working till here0')
    new_tags = list(set(new_tags))
    query_tokens.extend(new_tags)
    final_kg_node = {}
    print ('working till here1')
    current_elem = query_tokens[0]
    next_elem = query_tokens[1:]
    final_query = kg.query(query_tokens)
    print ('working till here2')
    for i in range(len(query_tokens)-1):
        z = final_query[current_elem]
        token_for_node = []
        print ('working till here3')
        for triplets in z:
            if triplets[0].lower() == current_elem.lower() and triplets[2].lower() in [x.lower() for x in next_elem]:
                token_for_node.append(triplets)
            if triplets[2].lower() == current_elem.lower() and triplets[0].lower() in [x.lower() for x in next_elem]:
                token_for_node.append(triplets)
        final_kg_node[current_elem] = token_for_node 
        current_elem = next_elem[0]
        next_elem = next_elem[1:]

    return final_kg_node, prompt

def gen_final(query, context):
    final_tok, prompt = gen_final_info(query, context, num_prompt = 5, tag = 'TEST')
    #final_prep_nodes = preprocessed_node(final_tok)
    qa = gen_sen(final_tok)
    return qa

'''if __name__ == "__main__":
    query = "How was Napoleon related to French Revolution and France?"
    context = "Napoleon (1769-1821) was a military and political leader of France who rose to prominence during the French Revolution and became the emperor of France from 1804 to 1814. He is widely regarded as one of the greatest military commanders in history, and his campaigns and conquests during the early 19th century greatly expanded the territory of France and reshaped the political landscape of Europe. Some of his most famous military campaigns include the Italian Campaign, the Egyptian Campaign, and the Napoleonic Wars. Despite his military successes, Napoleon's reign was marked by controversy and his rule ended in defeat and exile."
    #query = "Norepinephrine related to Neurotransmitter comes from an area of the brain known as what?"
    #context = "Napoleon Bonaparte was a military and political leader who rose to prominence during the French Revolution. He played a significant role in the events that unfolded during this period, ultimately leading to his rise to power as Emperor of France."
    #context = "There are dozens of other chemical neurotransmitter that are used in more limited areas of the brain, often areas dedicated to a particular function. Serotonin, for example\u2014the primary target of antidepressant drugs and many dietary aids\u2014comes exclusively from a small brainstem area called the Raphe nuclei. Norepinephrine, which is involved in arousal, comes exclusively from a nearby small area called the locus coeruleus. Other neurotransmitters such as acetylcholine and dopamine have multiple sources in the brain, but are not as ubiquitously distributed as glutamate and GABA."
    #ranked_doc = rank_corpus(query, context, 'spacy')
    
    #qa = gen_final(final_prep_nodes)
    #reframed_con = f"{context}{' '.join(qa)}"
    #print (f'Final Context: {reframed_con}')
    #prompt.append(query)
    #print (f'Final Propmt array: {prompt}')


'''


