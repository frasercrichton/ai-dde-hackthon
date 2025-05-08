from email import header
import pytest
import numpy as np

from src.database import RAGDatabase

from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level='DEBUG', catch=True)


class TestDatabase:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        logger.info('test')

    def test_load_records(self):


        # from sentence_transformers import SentenceTransformer

        # model = SentenceTransformer("thenlper/gte-small")  # Or your actual embedding model
        # text = "Aerial and satellite images admitted during former witness testimony are"
        # embedding = model.encode(text).tolist()  # Ensure it's a list

        # print(len(embedding))  # Should be 384
    
        # rag_database = RAGDatabase()
        document = (
            'Aerial and satellite images admitted during former witness testimony are'
        )

        # Generate a fake embedding of size 384
        embedding = np.random.rand(384).tolist()
        metadata = {
            'header': 'C. Aerial and Satellite Images',
            'subheader': 'C.4. Aerial and satellite images can be used to corroborate other evidence.',
            'context': 'C. Aerial and Satellite Images. C.2. Aerial and satellite images admitted during former witness testimony are',
        }

        rag_database.store_document(
            doc_id='doc_id_x1', document=document, embedding=embedding, metadata=metadata
        )

        x = rag_database.find_relevant_documents(
            'images',
            ['C. Aerial and Satellite Images'],
            [
                'C.4. Aerial and satellite images can be used to corroborate other evidence.'
            ],
            [
                'C. Aerial and Satellite Images. C.2. Aerial and satellite images admitted during former witness testimony are'
            ],
        )

        assert x == [
            {
                'text': 'Aerial and satellite images admitted during former witness testimony are',
                'id': 'doc_id_x1',
                'metadata': {
                    'context': 'C. Aerial and Satellite Images. C.2. Aerial and satellite images admitted during former witness testimony are',
                    'header': 'C. Aerial and Satellite Images',
                    'subheader': 'C.4. Aerial and satellite images can be used to corroborate other evidence.',
                },
            }
        ]
