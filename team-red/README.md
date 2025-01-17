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

# Data Cleaning

(Work in progress) PDF cleaning and markdown formatting.

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