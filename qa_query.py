from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch 
from gen_pmpt import gen_final
from evaluation import bleu

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

def gen_answer(question, context):
    ans = []
    for q in question:
        inputs = tokenizer(q, context, return_tensors="pt")
        # Generate the answer
        start_scores, end_scores = model(**inputs).values()
        start_index = torch.argmax(start_scores, dim=1).item()
        end_index = torch.argmax(end_scores, dim=1).item()
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_index:end_index+1]))
        ans.append(answer)
    return ans


if __name__ == "__main__":
    query = "How was Napoleon related to French Revolution and France?"
    context = "Napoleon Bonaparte was a military and political leader who rose to prominence during the French Revolution. He played a significant role in the events that unfolded during this period, ultimately leading to his rise to power as Emperor of France."
    #context = "Napoleon (1769-1821) was a military and political leader of France who rose to prominence during the French Revolution and became the emperor of France from 1804 to 1814. He is widely regarded as one of the greatest military commanders in history, and his campaigns and conquests during the early 19th century greatly expanded the territory of France and reshaped the political landscape of Europe. Some of his most famous military campaigns include the Italian Campaign, the Egyptian Campaign, and the Napoleonic Wars. Despite his military successes, Napoleon's reign was marked by controversy and his rule ended in defeat and exile."
    #query = "Norepinephrine related to Neurotransmitter comes from an area of the brain known as what?"
    #context = "There are dozens of other chemical neurotransmitter that are used in more limited areas of the brain, often areas dedicated to a particular function. Serotonin, for example\u2014the primary target of antidepressant drugs and many dietary aids\u2014comes exclusively from a small brainstem area called the Raphe nuclei. Norepinephrine, which is involved in arousal, comes exclusively from a nearby small area called the locus coeruleus. Other neurotransmitters such as acetylcholine and dopamine have multiple sources in the brain, but are not as ubiquitously distributed as glutamate and GABA."
    qa = gen_final(query, context)
    reframed_con = f"{context}{' '.join(qa)}"
    print (f'Final Context: {reframed_con}')
    prompt.append(query)
    print(f'Final Propmt array: {prompt}')

    print (gen_answer(prompt, reframed_con))
    reference_arr = [p.split() for p in qa]
    #calculate breu
    print (breu(reference_arr, ans))


