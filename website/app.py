import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import pipeline
from io import StringIO
import sys
sys.path.append('../')
import file_data as fd
import generate_kg as gkg
#import scrape_web as sw
#import gen_pmpt as genpmt
#import generate_embed as genemd
#import scrape_article as sart

#llm_pipeline = pipeline("question-answering", model="bert-base-cased")

def scrape_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text

def main():
    st.set_page_config(page_title="Know It More", page_icon=":books:", layout="wide")
    st.title("Know It More :books:")
    st.markdown("Get answers to your queries using powerful LLM models and Knowledge Graphs.")

    # Section 1
    st.subheader("Section 1: Query and Context")

    col1, col2 = st.columns([3, 3])

    with col1:
        query = st.text_input("Enter your query:")
        context = st.text_area("Enter context:")
        search = True
        query_tokens = []
        prompt = []
        if query != '' and context != '' and search:
            ranked_doc = genemd.rank_corpus(query, context, "spacy")
            #text = genpmt.gen_text(ranked_doc)
            #num_prompt = 5
            #imp_keywords = genpmt.get_keywords(text, num_prompt)
            print ('HELLOO----------------------')
            #model, tokenizer = genpmt.load_model()
            #for key in imp_keywords:
            #    ques = genpmt.get_question(text, key, model, tokenizer)
            #    prompt.append(ques)
            #    query_tokens.append(key.capitalize())
            #search = False
        

        #print(query_tokens)
        #print(prompt)
        if len(prompt) > 0:
            st.subheader("Possible Questions:")
            st.write(prompt[0])
            st.write(prompt[1])
            st.write(prompt[2])
            st.write(prompt[3])
            st.write(prompt[4])



    with col2:
        sub_col1, sub_col2, sub_col3 = st.columns([1, 1, 1])
        
        with sub_col1:
            kg_option = st.selectbox("Knowledge Graph:", ["Without KG", "With KG"])

        with sub_col2:
            llm_option = st.selectbox("LLM Model:", ["LLM 1", "LLM 2", "LLM 3"])

        with sub_col3:
            with st.form("answer_form"):
                submit_button = st.form_submit_button("Generate Answer")

        if submit_button:
            # Process the query and context with the LLM pipeline
            #result = llm_pipeline({'question': query, 'context': context})

            # Display the answer and confidence score
            st.subheader("Answer:")
            #st.write(result["answer"])
            
            #st.write("Confidence score:", result["score"])
            
        answer_area = st.empty()

    # Section 2
    st.subheader("Section 2: Document Upload and Knowledge Graph")
    col3, col4, col5 = st.columns(3)

    with col5:
        tag = None
        tag = st.text_input("Enter tag:").upper()

    with col3:
        import csv
        uploaded_file = st.file_uploader("Upload a document:")
        if uploaded_file is not None:
            file_name = uploaded_file.name
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            if tag == '':
                st.warning("Please type the tag for this content.")
            else:
                fd.read_file(string_data, tag)

    with col4:
        url = st.text_input("Enter the website URL:")
        if tag == '':
            st.warning("Please type the tag for this content.")

    if st.button("Generate KG"):
        # Process the document or URL and generate/update the Knowledge Graph (pseudocode)
        # This should be replaced with actual code to process the document or URL and generate/update the KG
        if uploaded_file or url:
            if uploaded_file:
                gkg.gen_kg(tag, file_path = f'../fetched_data/{tag}_dataset.csv',file_state = True)
            if url:
                print('hell0')
                #sart.scrape_url(url, tag)
                #gkg.gen_kg(tag, url_file_path = f'../fetched_data/{tag}_dataset.csv', url_state = True)
            st.success("Knowledge Graph has been generated/updated.")
            st.write(f"Generate KG can be viewed here /visualisation/{tag}.html")
        else:
            st.warning("Please upload a document or enter a URL.")

if __name__ == "__main__":
    main()
