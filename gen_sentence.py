import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

def gen_sen(kg_tokens):
    gen_sen_arr = []
    sen_arr = []
    for tok in kg_tokens.keys():
        for triplets in kg_tokens[tok]:
            entity_1, relation, entity_2 = triplets
            # Load pre-trained GPT-2 model and tokenizer
            tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            model = GPT2LMHeadModel.from_pretrained("gpt2")

            # Generate sentence
            input_text = f"{entity_1} is {relation} {entity_2}."
            input_ids = tokenizer.encode(input_text, return_tensors="pt")
            output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
            generated_sentence = tokenizer.decode(output[0], skip_special_tokens=True)
            gen_sen_arr.append(generated_sentence)
    for i in gen_sen_arr:
        sen_arr.append(i.split(".\n\n")[0])
    return sen_arr

#print(gen_sen({'Norepinephrine': [['Norepinephrine', 'related to', 'Neurotransmitter']]}))