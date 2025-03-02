import chromadb

class RAGDatabase:

    def __init__(self):
        """Initialize the document processor with necessary components."""  
        self.vector_db = chromadb.Client()
        self.collection = self.vector_db.get_or_create_collection(name="legal_docs")

    def store_document(self, doc_id, text, embedding, metadata={}):
        """Store document in the vector database."""
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def find_relevant_documents(self, query, headers, subheaders, context, n_results=3):
        """Find relevant documents for a given query."""

        print(f'find_relevant_documents query: {query} headers: {headers}, subheaders {subheaders}, context: {context}')

        filter_dict = {}

        if headers and len(headers) > 0:
          filter_dict["header"] = {"$in": headers}

        if subheaders:
          filter_dict["subheader"] = {"$in": subheaders}

        if context:
          filter_dict["context"] = {"$in": context}

        filter = None if len(filter_dict) == 0 else filter_dict

        print(f'***** filter: {filter}')

        return self.collection_query(query, filter, n_results)

    def collection_query(self, query, filter, n_results=3):
        """Find relevant documents for a given query."""

        results = self.collection.query(
            query_texts=[query],
            where=filter,
            n_results=n_results
        )
        print(f'collection_query : {results}')
        return [
            {
                'text': doc_text,
                'id': results['ids'][0][i],
                'metadata': results['metadatas'][0][i]
            }
            for i, doc_text in enumerate(results['documents'][0])
        ]

