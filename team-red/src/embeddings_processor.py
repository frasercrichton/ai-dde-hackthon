from transformers import AutoModel
from src.tokenizer import Tokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import torch
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


# EmbeddingHandler
class EmbeddingsProcessor:

    # TinyLlama/TinyLlama-1.1B
    # MODEL = 'meta-llama/Llama-3.1-8B'
    # embeddings_processor = EmbeddingsProcessor('sentence-transformers/all-MiniLM-L6-v2')

    def __init__(self, model_name, tokenizer):
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.tokenizer = tokenizer

    def create_embeddings(self, text):

        inputs = self.tokenizer.tokenize(text)

        if torch.cuda.is_available():
            logger.info('cuda available')
            self.model.to('cuda')
        else:
            logger.warning('cuda not available!')

        inputs = {k: v.to('cuda') for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()


# from transformers import AutoTokenizer, AutoModel
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import torch

# class EmbeddingsProcessor:


#     # embeddings_processor = EmbeddingsProcessor('sentence-transformers/all-MiniLM-L6-v2')

#     def __init__(self, model_name):

#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModel.from_pretrained(model_name)
#         self.model.eval()


#     def create_embeddings(self, text):
# 1) tokenize teh text
#         inputs = self.tokenizer(
#             text,
#             return_tensors='pt',
#             truncation=True
#         )
#         # logger.info(f'inputs: {inputs}')

# 2) take teh inputs and create a list of embeddings
#         if torch.cuda.is_available():
#             logger.info('cuda available')
#             self.model.to('cuda')
#             inputs = {k: v.to('cuda') for k, v in inputs.items()}
#         else:
#             logger.warning('cuda not available!')


#         with torch.no_grad():
#             outputs = self.model(**inputs)

#         return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()
