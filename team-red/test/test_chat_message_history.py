from email import header
import pytest
import numpy as np
from requests import TooManyRedirects
from sympy import pretty_print
from src.chat_message_history_builder import ChatMessageHistoryBuilder
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level='DEBUG', catch=True)


class TestChatMessageHistoryBuilder:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        logger.info('test')

    def test_message_history(self):

        chat_message_history_builder = ChatMessageHistoryBuilder()
        chat_message_history_builder.add_message(
            'user', 'How is digital evidence authenticated?'
        )
        chat_message_history_builder.add_message(
            'assistant',
            "According to the document, it's verified via chain of custody and metadata.",
        )
        assert (
            chat_message_history_builder._convert_to_llama_format()
            == "<|begin_of_text|><|start_header_id|>user<|end_header_id|>How is digital evidence authenticated?<|eot_id|><|start_header_id|>assistant<|end_header_id|>According to the document, it's verified via chain of custody and metadata.<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        )

    def test_message_history(self):

        chat_message_history_builder = ChatMessageHistoryBuilder()
        chat_message_history_builder.add_message(
            'user', 'How is digital evidence authenticated?'
        )
        chat_message_history_builder.add_message(
            'assistant',
            "According to the document, it's verified via chain of custody and metadata.",
        )
        prompt = chat_message_history_builder.build_prompt(
            retrieved_context='This is a legal document. It contains information about the case XYZ v. ABC. The case was decided in 2020 and is relevant to the current discussion.',
            question='How is digital evidence authenticated?',
        )
        assert (
            prompt
            == """<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a helpful legal assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>How is digital evidence authenticated?<|eot_id|><|start_header_id|>assistant<|end_header_id|>According to the document, it's verified via chain of custody and metadata.<|eot_id|><|start_header_id|>user<|end_header_id|>Context:
This is a legal document. It contains information about the case XYZ v. ABC. The case was decided in 2020 and is relevant to the current discussion.

Question: How is digital evidence authenticated?<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        )
