import chromadb
import logging
logger = logging.getLogger(__name__)
      


class VectorDatabase:


    client = None

    def __init__(self, collection_name):
        logger.info('Initialising.')

        if VectorDatabase.client is None:
            logger.info('RAGDatabase.client is none.')
            VectorDatabase.client = chromadb.Client()
            self.client = VectorDatabase.client

        # logger.info('Resetting.')
        # self.client.reset()
        self.collection = self.client.get_or_create_collection(name=collection_name)


    def store_document(self, doc_id, document, embedding, metadata={}):
        """Store document in the vector database."""
        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id],
        )

    # def store_documents(self, documents: list):

    #     kwargs = {
    #         "documents": [doc.get('text') for doc in documents],
    #         "embeddings": [doc.get('embedding') for doc in documents],
    #         "ids": [doc.get('id') for doc in documents]
    #     }

    #     metadata = [doc.get('metadata', {}) for doc in documents if doc.get('metadata') is not None]
    #     if len(metadata) > 0:
    #         kwargs["metadatas"] = metadata

    #     try:
    #         self.collection.add(**kwargs)
    #     except Exception as e:
    #         logging.error(f"Error adding documents: {e}")

    def get_collection(self, collection_name):
        collection = self.client.get_collection(collection_name)
        return collection.get()

    def query_with_embeddings(self, embedding_query, metadata_query=None, n_results=3):

# n_results=3 to 5 is generally a safe default for most applications.
# What If My Top n_results Are Not Useful?
# 	•	Increase the embedding quality → Use a better embedding model or fine-tune one.
# 	•	Apply re-ranking → Use a second model to score and reorder the results.
# 	•	Filter results by metadata → If using ChromaDB with metadata, filter based on relevant categories (e.g., category="landmarks").
# 	•	Use hybrid retrieval → Combine keyword-based search with embeddings for better results.

        # n_results=3
        # high precision 1-3
  #       Works well when information may be spread across multiple short documents.
	# •	Example: Answering questions that require synthesizing different perspectives, like a summary of multiple research papers.

        # more context 3 to 5
  #       # high recall (broad retrieval for re-ranking) 5 to 10+
  #       Recommended when re-ranking or filtering is applied after retrieval.
	# •	Example: Open-domain Q&A systems where an LLM will decide the most relevant information after fetching multiple candidates.

        query = {
            'query_embeddings': embedding_query,
            'n_results': n_results
        }

        if metadata_query:
            query['where'] = metadata_query

        logger.info(f'query {query}')


        results = self.collection.query(**query)

        logger.info(results)

        # Here’s the logic for this:
        #   •	Lower distances indicate higher similarity (the documents are more relevant).
        #   •	Higher distances indicate lower similarity (the documents are less relevant).
        threshold = 50.0
        distances = results['distances'][0]

        if min(distances) > threshold:
            print(f'No relevant documents found (Distances {distances}).')
            return [{
                'text': 'No relevant documnts found for this query',
                'id': 'unknown',
                'metadata': {}
            }]
        else:
            print(f'Proceed with RAG... {distances}')

        return [
            {
                'text': doc_text,
                'id': doc_id,
                'metadata': doc_metadata
            }
            for doc_text, doc_id, doc_metadata in zip(results['documents'][0], results['ids'][0], results['metadatas'][0])
        ]

    # def query_with_text(self, query, filter, n_results=3):

    #     results = self.collection.query(
    #         query_texts=[query], where=filter, n_results=n_results
    #     )
    #     return [
    #         {
    #             'text': doc_text,
    #             'id': results['ids'][0][i],
    #             'metadata': results['metadatas'][0][i],
    #         }
    #         for i, doc_text in enumerate(results['documents'][0])
    #     ]
# **************


    def find_relevant_documents(
        self,
        query: str,
        headers: list = [],
        subheaders: list = [],
        context: list = [],
        n_results=3,
    ):
        """Find relevant documents for a given query."""

        # print(
        #     f'find_relevant_documents query: {query} headers: {headers}, subheaders {subheaders}, context: {context}'
        # )

        filter_dict = {}

        if headers:
            filter_dict['header'] = {'$in': headers}

        if subheaders:
            filter_dict['subheader'] = {'$in': subheaders}

        if context:
            filter_dict['context'] = {'$in': context}

        # If filter_dict is not empty, transform it into an OR query correctly
        if filter_dict:
            filter_dict = {'$or': [{key: value} for key, value in filter_dict.items()]}
        else:
            filter_dict = None  # Keep None when no filters exist
        # print(f'***** filter: {filter_dict}')

        return self.collection_query(query, filter_dict, n_results)

    #   def collection_embedding_query(self, query, filter, n_results=3):

    # query_embedding = generate_embedding("satellite images")

    # results = self.collection.query(
    #     query_embeddings=[query_embedding], where=filter_dict, n_results=3
    # )

    def collection_query(self, query, filter, n_results=3):
        """Find relevant documents for a given query."""

        results = self.collection.query(
            query_texts=[query], where=filter, n_results=n_results
        )
        # print(f'collection_query : {results}')
        return [
            {
                'text': doc_text,
                'id': results['ids'][0][i],
                'metadata': results['metadatas'][0][i],
            }
            for i, doc_text in enumerate(results['documents'][0])
        ]

    def delete_collection(self, collection_name):
        self.client.delete_collection(collection_name)

    def reset_database(self):
        self.client.reset()
