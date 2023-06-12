## Inspiration
So I was once talking to a person on the train about how GPT4 and chatGPT are revolutionizing several day-to-day tasks such as writing blogs or getting answers for several questions but soon being a security guy he pointed a question whatever chatGPT returns is an uncontrolled knowledge and more like inappropriate out of context answer (sometimes). This hit me hard as it was a true statement, so I started thinking about how I could power this or make it more controlled. Doing a bit of research into this I read about LLMs, PLMs, Question Answering, and entities recognition. Soon I got an idea to make it more controlled based on how we humans learn things. Why not provide it with a set of knowledge which will set up a boundary for it to make the answers prediction? It will make it controlled or basically bind it under certain knowledge. One of the other challenges was as soon as we start learning and moving forward we tend to forget things easily so you can ask questions about the things that you have learned and it will act as an E-Brain and help you to remind stuff. I am also using Pangea wrapper APIs at most of the places to perform checks such as checking the upload file, URLs, queries, and contexts, and soon going to integrate it with the authentication flow for users.
 
## What it does
So it is a centralized platform where users like researchers, students, or anyone who wants to perform QA can upload their documents like notes or articles like web URLs or resources by which this platform is going to make a knowledge graph that is going to set the boundary of these answers. Once the knowledge graph is created the user can ask questions providing a context. Further, this question and context will pass through a few steps basically to make the context more driven towards the query for example what if the query is **how to make mango cheesecake** and the context might be about cheesecake, mango, and cakes in general**. So the platform will make the context more driven toward the question. Further, it will query the knowledge graph to extract information and that will help in making the context more driven towards our controlled idea based on the topic. And once all of this is done I used a few other automatic question generation techniques to make more questions out of it which will be further asked to an LLM generating the more meaningful answer. One of the other benefits of this is that users can upload their pdfs or documents and it will automatically generate questions for them as a reference from the document.

## Pangea Wrapper
I am also using Pangea wrapper apis at most of the places to perform checks such as checking the upload file, urls, queries, contexts, and also integrated it with the authentication flow for users. Some use of APIs are - 
- Sign up and Sign in -> I used Auth APIs here to create signin and signup flow for the web app which maintains the user signin and signup states easy.
- File check -> To check if the uploaded file is malicious or not I used file intel apis.
- URL check -> To check if the URL is malicious or not I used url intel apis
- Text Check -> To check if the text in the query and context is malicious or not I used the redact apis
- IP check -> To check if the ip is malicios I used ip intel apis


## How we built it
There are a few steps that I have done to  make this work - 
- To generate KG I used the REBEL model to extract the entities from the sentences which are further added as a node and relations as edges of the graph. I used pyvis library to visualize the KG.
- To make the context more driven toward the query I basically first tokenized the context and further used sentence similarity algorithms such as cosine similarity to rank the sentences inside the context based on the question. Further, I take top N sentences and generate the ranked context. To get the cosine similarity done I used several embedding techniques such as word embedding, word2vec, and tfidf (word2vec was best in my case).
- Next, I extracted entities from the question and used them to query KG to generate meaningful nodes, here I also used node2vec and word2vec embeddings to extract similar nodes such as **Napoleon Bonaparte** and **Napoleon**. Once I extracted the triplets i.e. entity1, entity2, and the relation between them. I further generated meaningful sentences from it using key2text models such as T5. These extra-generated sentences were further added to the ranked context. 
- Further, I used the extracted keyword to generate the extra questions from the query which is further added to the initial question. 
- As of now we have a question list from just one question and more query-directed and controlled context with the help of context and KG. So Now I pass it to my own trained QA model to generate a more meaningful answer. Also, the normal QA models just answer in one or two words but it actually makes it more helpful as it provides a detailed answer.
- To make this whole process simpler I made the web platform using Streamlit which actually makes it easy to access.
## Challenges we ran into
The main challenge was to train this on my local machine. The biggest challenge was to create dense KG.

## Accomplishments that we're proud of
I am proud of first solving the problem of generating more controlled answers and taking one step closed to the world of controlled QA. The other thing of which I am proud is basically generating dense KG, I made the approach to update the KG. So initially it will create the KG for a particular batch size and further, it will update the same KG iteratively to make it more dense and knowledgable. I also used a tag word for the same type of document which will add up information in the same KG such as SpaceX and Falcon9 can have the same keyword as either SpaceX or space.

## What we learned
Here I mainly learned about how to develop software products that solve a real problems. Due to the rise of AI and GPTs there is a need to make them more controlled and safe. This project opened up my eye to fixing several more loopholes in the same field such as the security of these data and models.

## What's next for Know it more
Next, I am going to make the LLM more powerful, optimize the KG, and will try to add more resources to extract data based on trusted web platforms for specific fields such as for maybe AI, I will go with websites such as Google Scholar, FB research, Google AI article, and etc.
