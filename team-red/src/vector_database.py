import chromadb
import logging

class VectorDatabase:

    
    def __init__(self):
        """Initialize the document processor with necessary components."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.vector_db = chromadb.Client()
        self.collection = self.vector_db.get_or_create_collection(name='legal_docs')

    def store_document(self, doc_id, document, embedding, metadata={}):
        """Store document in the vector database."""
        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id],
        )

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
