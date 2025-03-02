from email import header
import pytest

from src.database import RAGDatabase

from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="DEBUG", catch=True)


class TestDatabase:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        logger.info("test")



    def test_load_records(self):
        rag_database = RAGDatabase()
        text = (
            "Aerial and satellite images admitted during former witness testimony are"
        )
        embedding = ""
        metadata = {
            "header": "C. Aerial and Satellite Images",
            "subheader": "C.4. Aerial and satellite images can be used to corroborate other evidence.",
            "context": "C. Aerial and Satellite Images. C.2. Aerial and satellite images admitted during former witness testimony are",
        }

        rag_database.store_document(
            doc_id="doc_id_x1", text=text, embedding=embedding, metadata=metadata
        )
        # records = channel_CSV.get_records(path='test/data/channels.csv')
        assert len([]) == 7
