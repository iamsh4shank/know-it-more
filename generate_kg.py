# needed to load the REBEL model
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import math
import torch
# wrapper for wikipedia API
import wikipedia

# graph visualization
from pyvis.network import Network

# show HTML in notebook
import IPython
import csv
import importlib
from os import path as osp
import os
import logging
import pickle

# configure the logging module
logging.basicConfig(filename='example.log', level=logging.DEBUG)


# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")

def extract_relations_from_model_output(text):
    relations = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    text_replaced = text.replace("<s>", "").replace("<pad>", "").replace("</s>", "")
    for token in text_replaced.split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        relations.append({
            'head': subject.strip(),
            'type': relation.strip(),
            'tail': object_.strip()
        })
    return relations

# knowledge base class
class KG():
    def __init__(self):
        self.entities = {}
        self.relations = []

    def are_relations_equal(self, r1, r2):
        return all(r1[attr] == r2[attr] for attr in ["head", "type", "tail"])

    def exists_relation(self, r1):
        return any(self.are_relations_equal(r1, r2) for r2 in self.relations)

    def merge_relations(self, r1):
        r2 = [r for r in self.relations
              if self.are_relations_equal(r1, r)][0]
        spans_to_add = [span for span in r1["meta"]["spans"]
                        if span not in r2["meta"]["spans"]]
        r2["meta"]["spans"] += spans_to_add
    
    def get_wikipedia_data(self, candidate_entity):
        try:
            page = wikipedia.page(candidate_entity, auto_suggest=False)
            entity_data = {
                "title": page.title,
                "url": page.url,
                "summary": page.summary
            }
            return entity_data
        except:
            return None

    def add_entity(self, e):
        self.entities[e["title"]] = {k:v for k,v in e.items() if k != "title"}

    def add_relation(self, r):
        # check on wikipedia
        candidate_entities = [r["head"], r["tail"]]
        entities = [self.get_wikipedia_data(ent) for ent in candidate_entities]

        # if one entity does not exist, stop
        if any(ent is None for ent in entities):
            return

        # manage new entities
        for e in entities:
            self.add_entity(e)

        # rename relation entities with their wikipedia titles
        r["head"] = entities[0]["title"]
        r["tail"] = entities[1]["title"]

        # manage new relation
        if not self.exists_relation(r):
            self.relations.append(r)
        else:
            self.merge_relations(r)

    def merge_kg(self, kg2):
        for r in kg2.relations:
            self.add_relation(r)
            
    def print(self):
        print("Entities:")
        for e in self.entities.items():
            print(f"  {e}")
        print("Relations:")
        for r in self.relations:
            print(f"  {r}")

    def get_entities(self):
        nodes_entity = []
        for k in self.entities.keys():
            nodes_entity.append(k)
        return nodes_entity

    def merge_with_kg(self, kg2):
        for r in kg2.relations:
            self.add_relation(r)

    def query(self, tags):
        prompts_tag = {}
        for tag in tags:
            triplet = []
            print (tag)
            for r in self.relations:
                if str(tag).lower() in str(r['head']).lower() or str(tag).lower() in str(r['tail']).lower():
                    triplet.append([r['head'], r['type'], r['tail']])
            prompts_tag[tag] = triplet
        return prompts_tag


# extract relations for each span and put them together in a knowledge base
def from_text_to_kg(text_arr, kg_name = None, span_length=128, verbose=False):
    
    text = " ".join(text_arr)
    inputs = tokenizer([text], return_tensors="pt")


    # compute span boundaries
    num_tokens = len(inputs["input_ids"][0])
    if verbose:
        print(f"Input has {num_tokens} tokens")
    num_spans = math.ceil(num_tokens / span_length)
    if verbose:
        print(f"Input has {num_spans} spans")
    overlap = math.ceil((num_spans * span_length - num_tokens) / 
                        max(num_spans - 1, 1))
    spans_boundaries = []
    start = 0
    for i in range(num_spans):
        spans_boundaries.append([start + span_length * i,
                                 start + span_length * (i + 1)])
        start -= overlap
    if verbose:
        print(f"Span boundaries are {spans_boundaries}")

    # transform input with spans
    tensor_ids = [inputs["input_ids"][0][boundary[0]:boundary[1]]
                  for boundary in spans_boundaries]
    tensor_masks = [inputs["attention_mask"][0][boundary[0]:boundary[1]]
                    for boundary in spans_boundaries]
    inputs = {
        "input_ids": torch.stack(tensor_ids),
        "attention_mask": torch.stack(tensor_masks)
    }

    # generate relations
    num_return_sequences = 3
    gen_kwargs = {
        "max_length": 256,
        "length_penalty": 0,
        "num_beams": 3,
        "num_return_sequences": num_return_sequences
    }
    generated_tokens = model.generate(
        **inputs,
        **gen_kwargs,
    )

    # decode relations
    decoded_preds = tokenizer.batch_decode(generated_tokens,
                                           skip_special_tokens=False)

    if kg_name:
        kg = kg_name
    else:
        # create kg
        kg = KG()
    i = 0
    for sentence_pred in decoded_preds:
        current_span_index = i // num_return_sequences
        relations = extract_relations_from_model_output(sentence_pred)
        for relation in relations:
            relation["meta"] = {
                "spans": [spans_boundaries[current_span_index]]
            }
            kg.add_relation(relation)
        i += 1

    return kg

def save_network_html(kg, filename="network.html"):
    # create network
    net = Network(directed=True, width="700px", height="700px")

    # nodes
    color_entity = "#FFFF99"
    for e in kg.entities:
        net.add_node(e, shape="circle", color=color_entity)

    # edges
    for r in kg.relations:
        net.add_edge(r["head"], r["tail"],
                    title=r["type"], label=r["type"])

    # save network
    net.repulsion(
        node_distance=200,
        central_gravity=0.2,
        spring_length=200,
        spring_strength=0.05,
        damping=0.09
    )
    net.set_edge_smooth('dynamic')
    net.save_graph(filename)

def save_kg(kg, filename):
    with open(filename, "wb") as f:
        pickle.dump(kg, f)

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'KG':
            return KG
        return super().find_class(module, name)

def load_kg(filename):
    res = None
    with open(filename, "rb") as f:
        res = CustomUnpickler(f).load()
    return res

def read_csv(file_path):
    with open(f'{file_path}', newline='') as csvfile:
        reader = csv.reader(csvfile)
        file_content = []
        for row in reader:
            file_content.append(row[0])
    return file_content

def gen_kg(tag, url_file_path = None, file_path = None, file_state = False, url_state = False):
    """It can be used to generate KG from the content

    Args:
        tag (_type_): string
        url_file_path (_type_, optional): csv path for the url. Defaults to None.
        file_path (_type_, optional): csv path for the file. Defaults to Nonefile_state=True.
        url_state (bool, optional): It will act as a switch to add url KG generation. Defaults to True.
        file_state (bool, optional): It will act as a switch to add file KG generation. Defaults to True.
    """
    if file_state:
        file_content = read_csv(file_path)
        if len(file_content) > 25:
            batch_size = 25
            kg = from_text_to_kg(file_content[0:25], verbose=True)
            for i in range(25, len(file_content), batch_size):
                kg = from_text_to_kg(file_content[i:i+batch_size], kg_name = kg, verbose=True)
                #kg1 = from_text_to_kg(file_content[i:i+batch_size], verbose=False)
                #kg = kg.merge_with_kg(kg1)    
                save_network_html(kg, filename=f'visualisation/{tag}.html')
                save_kg(kg, f'gen_KG/{tag}.pkl')
                print("batch {} saved".format(i))
        else:
            kg = from_text_to_kg(file_content, verbose=True)
            save_network_html(kg, filename=f'visualisation/{tag}.html')
            save_kg(kg, f'gen_KG/{tag}.pkl')
    if url_state:
        url_file_content = read_csv(url_file_path)
        kg = from_text_to_kg(url_file_content, verbose=True)
        save_network_html(kg, filename=f'visualisation/{tag}.html')
        save_kg(kg, f'gen_KG/{tag}.pkl')

    if file_state and url_state:
        file_content = read_csv(file_path)
        url_file_content = read_csv(url_file_path)
        kg = from_text_to_kg(file_content, verbose=True)
        kg = from_text_to_kg(url_file_content, kg_name = kg, verbose=True)
        save_network_html(kg, filename=f'visualisation/{tag}.html')
        save_kg(kg, f'gen_KG/{tag}.pkl')

    logging.info('Knowledge Graph generated successfully')
    return 0

def update_kg(tag, file_content, url_file_content, file_state = True, url_state = True):
    """It can be used to update the KG

    Args:
        tag (_type_): string
        url_file_content (_type_, optional): array for the url. Defaults to None.
        file_content (_type_, optional): array for the file. Defaults to Nonefile_state=True.
        url_state (bool, optional): It will act as a switch to add url KG generation. Defaults to True.
        file_state (bool, optional): It will act as a switch to add file KG generation. Defaults to True.
    Returns:
        _type_: _description_
    """
    kg = load_kg(f'gen_KG/{tag}.pkl')
    if file_state:
        #kg = from_text_to_kg(file_content, kg_name = kg, verbose=True)
        save_network_html(kg, filename=f'visualisation/{tag}.html')
        save_kg(kg, f'gen_KG/{tag}.pkl')
        
    if url_state:
        kg = from_text_to_kg(url_file_content, kg_name = kg, verbose=True)
        save_network_html(kg, filename=f'visualisation/{tag}.html')
        save_kg(kg, f'gen_KG/{tag}.pkl')

    logging.info('Knowledge Graph updated successfully')
    return 0

if __name__ == '__main__':
    # To generate KG from the content
    gen_kg('TEST', file_path = 'fetched_data/TEST_dataset.csv', file_state = True)  
    print("Processing complete.")