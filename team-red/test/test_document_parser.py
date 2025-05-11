from email import header
import pytest
import numpy as np
from src.document_parser import DocumentParser
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level='DEBUG', catch=True)


class TestDocumentParser:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        logger.info('test')

    def test_preprocess_documents_for_chroma(self):
        document_parser = DocumentParser()

        leiden_documents = [
            {
                'metadata': {
                    'headers': 'VIDEOS',
                    'tags': [
                        'no excerpts',
                        'entire video',
                    ],
                },
                'text': 'the video excerpts',
            }
        ]

        formatted_documents = document_parser.preprocess_documents_for_chroma(
            leiden_documents
        )
        print(formatted_documents)
        assert formatted_documents == [
            {
                'metadata': {
                    'headers': 'VIDEOS',
                    'no excerpts': True,
                    'entire video': True,
                },
                'text': 'the video excerpts',
            }
        ]
