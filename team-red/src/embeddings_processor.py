from transformers import AutoModel
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
