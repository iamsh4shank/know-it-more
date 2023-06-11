# Research Assistant Web App 

The Research Assistant Web App is a Streamlit-based web application that leverages Language Models (LLMs) and Knowledge Graphs (KGs) to answer your queries.

## Deployment for Development

### Prerequisites

- Python 3.6 or higher
- Pip (Python package manager)

### Steps to Deploy

1. Clone the repository or download the files containing the web app code.
2. Navigate to the project directory in the terminal or command prompt.
3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```


Here's a markdown guide explaining how to deploy the UI in development and its usage:

markdown
Copy code
# Research Assistant Web App

The Research Assistant Web App is a Streamlit-based web application that leverages Language Models (LLMs) and Knowledge Graphs (KGs) to answer your queries.

## Deployment for Development

### Prerequisites

- Python 3.6 or higher
- Pip (Python package manager)

### Steps to Deploy

1. Clone the repository or download the files containing the web app code.
2. Navigate to the project directory in the terminal or command prompt.
3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
Run the Streamlit web app:
```

4. Run the Streamlit web app:

```bash
streamlit run app.py
```

5. The web app should now be accessible in your browser at http://localhost:8501.

### Usage
#### Section 1: Query and Context
1. Enter your query: Input the question you want the LLM to answer.
2. Enter context: Provide additional context to help the LLM generate a more accurate answer. This can be a paragraph or a few sentences containing relevant information.
3. Knowledge Graph: Choose between "With KG" and "Without KG" to decide whether or not to use the Knowledge Graph in generating the answer.
4. LLM Model: Select the desired LLM model from the available options.
5. Click the "Generate Answer" button to process the query and context. The answer, along with a confidence score, will be displayed in the text area below the button.

#### Section 2: Document Upload and Knowledge Graph
1. Upload a document: Upload a file containing text that you want to use for creating or updating the Knowledge Graph. Supported formats include .txt, .pdf, and .docx.
2. Enter the website URL: Alternatively, you can input a URL to scrape text from a web page for generating or updating the Knowledge Graph.
3. Enter tags (comma-separated): Provide relevant tags to categorize and organize the information in the Knowledge Graph.
4. Click the "Generate KG" button to process the uploaded document or URL and generate/update the Knowledge Graph. A success message will be displayed upon completion.

#### Note
This is a development deployment guide. For production deployment, please refer to the Streamlit Deployment Guide.

This markdown file provides instructions for deploying the Research Assistant Web App in a development environment and explains its usage in a clear and concise manner.
