# AI and Digital Evidence Hackathon

This is a spike to build out a proof of concept Chat Bot that uses the [Leiden Guidelines](https://leiden-guidelines.netlify.app/guidelines/) to provide guidance on Digitally Derived Evidence (DDE) used in international criminal courts and tribunals to prosecute perpetrators of international crime

The chat bot is intended to provide different people with access to advice based on their role. 

User interface: 

![](./images/Screenshot%202025-01-17%20at%2011.22.58 AM.png)

Note: the current chat bot hallucinates and has a significant issue with document retrieval which needs worked on to productionise the bot.

## Vision

![](./images/Screenshot%202025-01-17%20at%2011.41.35 AM.png)

![](./images/Flow%20drop%20app%20slideshow%20(Community).jpg)

## Running

Run the hackathon.ipynb Jupyter Notebook. 

Pip Local Environment

```
python3 -m venv env

source env/bin/activate
```

Check it:

```
which python

python3 -m pip install -r requirements.txt
```

Deactivate
```
deactivate
```

# Data Cleaning

(Work in progress) PDF cleaning and markdown formatting.

Run the pdf-processor.ipynb.

## Chroma 

n_results=3 to 5 is generally a safe default for most applications.
What If My Top n_results Are Not Useful?
- Increase the embedding quality → Use a better embedding model or fine-tune one.
- Apply re-ranking → Use a second model to score and reorder the results.
- Filter results by metadata → If using ChromaDB with metadata, filter based on relevant categories (e.g., category="landmarks").
- Use hybrid retrieval → Combine keyword-based search with embeddings for better results.

        n_results=3
        high precision 1-3
        Works well when information may be spread across multiple short documents.
- Example: Answering questions that require synthesizing different perspectives, like a summary of multiple research papers.

        more context 3 to 5
        high recall (broad retrieval for re-ranking) 5 to 10+
        Recommended when re-ranking or filtering is applied after retrieval.
- Example: Open-domain Q&A systems where an LLM will decide the most relevant information after fetching multiple candidates.

Here’s the logic for this:
    •	Lower distances indicate higher similarity (the documents are more relevant).
    •	Higher distances indicate lower similarity (the documents are less relevant).


### For the future

The RAG database needs small fragments rather than complete documents so that it will work within the token limits. Each fragment needs metadata attached to assist querying. A pipeline that can parse each document, extract metadata and chunk the fragments is required possibly based on this flow:       

![](./images/Drawing%202025-01-17%2008.58.08.excalidraw.png)

Currently the notebook uses Regex to query for the chunks but it might be possible to train an LLM to do this which would work better for different document formats.   


# Training

Run the training.ipynb Notebook with the fine_tuning_leiden_guidelines.jsonl data.

### For the future

A framework to automate question generation from a document for   

![](./images/Drawing%202025-01-17%2010.03.27.excalidraw.png)


This could be augmented with some example questions and some kind of editor for teh human reviewer to be able to remove bad res


# TODOS and Improvements

- extract code from Jupyter Note books and create a Python application that can be run as a pipeline 