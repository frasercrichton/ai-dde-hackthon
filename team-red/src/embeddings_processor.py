from transformers import AutoTokenizer, AutoModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
import torch
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class EmbeddingsProcessor:
    
    # embeddings_processor = EmbeddingsProcessor('sentence-transformers/all-MiniLM-L6-v2')

    def __init__(self, model_name):
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()


    def create_embeddings(self, text):
            
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True
        )
        # logger.info(f'inputs: {inputs}')

        if torch.cuda.is_available():
            logger.info('cuda available')
            self.model.to('cuda')
            inputs = {k: v.to('cuda') for k, v in inputs.items()}
        else:
            logger.warning('cuda not available!')
          

        with torch.no_grad():
            outputs = self.model(**inputs)

        return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()
        