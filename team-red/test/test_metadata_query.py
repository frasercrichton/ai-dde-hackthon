from email import header
import pytest
import numpy as np
from src.metadata_query import MetadataQuery
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level='DEBUG', catch=True)


class TestMetadataQuery:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        logger.info('test')

    def test_create_headers(self):
        metadata_query = MetadataQuery()
        assert metadata_query.createFilters(headers=['header one', 'header two']) == {
            '$or': [
                {'headers': {'$in': ['header one', 'header two']}},
            ]
        }

    def test_create_single_header(self):
        metadata_query = MetadataQuery()
        assert metadata_query.createFilters(headers=['header one']) == {
            'headers': 'header one'
        }

    def test_create_single_tag(self):
        metadata_query = MetadataQuery()
        assert metadata_query.createFilters(tags=['header one']) == {
            'header one': True
        }

    def test_create_tags(self):
        metadata_query = MetadataQuery()
        assert metadata_query.createFilters(tags=['one', 'two']) == {
            '$or': [{'one': True}, {'two': True}]
        }

    def test_create_headers_and_tags(self):
        metadata_query = MetadataQuery()
        assert metadata_query.createFilters(
            headers=['header one', 'header two'], tags=['one']
        ) == {
            '$or': [
                {'headers': {'$in': ['header one', 'header two']}},
                {'one': True},
            ]
        }

    def test_create_single_headers(self):
        metadata_query = MetadataQuery()
        assert metadata_query.createFilters(headers=['header one'], tags=['one']) == {
            'headers': {'$in': ['header one']}
        }

    def test_create_single_headers(self):
        metadata_query = MetadataQuery()
        assert metadata_query.createFilters(
            headers=['VIDEOS'], tags=['working language', 'court language']
        ) == {
            '$or': [
                {'headers': {'$in': ['VIDEOS']}},
                {'working language': True},
                {'court language': True},
            ]
        }
