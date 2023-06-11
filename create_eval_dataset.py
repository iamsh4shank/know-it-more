from datasets import load_dataset
import json
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG)

def adversarialQA(small_dict, title = 'brain'):
    dataset = load_dataset("adversarial_qa", 'adversarialQA')
    small_dict = {}
    for i in range(30000):
        if dataset["train"][i]['title'].lower() == title:
            # title, question, answers, context
            small_dict[i] = [dataset["train"][i]['title'] , dataset["train"][i]['question'], dataset["train"][i]['answers'], dataset["train"][i]['context']]
        
    return small_dict

def squadQA(small_dict, title = 'brain'):
    dataset = load_dataset("squad")
    ground_val = 0
    val_switch = False
    for i in range(87599):
        if (val_switch is False) and (dataset["train"][i]['title'].lower() == 'brain'):
            val_switch = True
            ground_val = i
        if dataset["train"][i]['title'].lower() == title:
            # title, question, answers, context
            small_dict[i-ground_val] = {"title": dataset["train"][i]['title'] , 
                                        "question": dataset["train"][i]['question'], 
                                        "answer": dataset["train"][i]['answers'],
                                        "context": dataset["train"][i]['context']
                                        }    
    return small_dict

if __name__ == '__main__':
    small_dict = {}
    small_dict = adversarialQA(small_dict)
    small_dict = squadQA(small_dict)
    with open('output/eval/output.json', 'w') as f:
        json.dump(small_dict, f, indent=4)
    logging.info('Completed')
    


