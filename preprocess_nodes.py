import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

# Load tokenizer and pre-trained language model
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

def remove_duplicates(nested_list):
    result = []
    seen = set()
    for sublist in nested_list:
        key = tuple(sublist[:2])
        if key not in seen:
            seen.add(key)
            result.append(sublist)
    return result

def get_node_embeddings(node_triplet):
    node_text = " ".join(node_triplet)
    inputs = tokenizer(node_text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    return torch.mean(outputs.last_hidden_state, dim=1).squeeze()

def preprocessed_node(kg_nodes):
    final_nodes = {}
    for node_name in kg_nodes.keys():
        remaining_nodes = []
        node_triplets = kg_nodes[node_name]
        if node_triplets != []:
            current_elem = node_triplets[0]
            next_elem = node_triplets[1:]
            for i in range(len(node_triplets)-1):
                similarity = [cosine_similarity(get_node_embeddings(current_elem).detach().numpy().reshape(1,-1), get_node_embeddings(other_node).detach().numpy().reshape(1,-1) )[0][0] for other_node in next_elem]
                for sim in similarity:
                    if sim >0.8:
                        idx = similarity.index(sim)
                        if (next_elem[idx] in remaining_nodes):
                            remaining_nodes.remove(next_elem[idx])
                        next_elem.remove(next_elem[idx])

                if len(next_elem)!=0:    
                    remaining_nodes.extend([current_elem])
                    remaining_nodes.extend(next_elem)
                    current_elem = next_elem[0]
                    next_elem = next_elem[1:]
        final_nodes[node_name] = remove_duplicates(remaining_nodes)
    return final_nodes
