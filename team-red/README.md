# AI and Digital Evidence Hackathon

## Running

Run the Jupyter Notebook 


Vision


# Data Cleaning

Work in progress PDF cleaning and markdown formatting.

Run the pdf-processor.ipynb.

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