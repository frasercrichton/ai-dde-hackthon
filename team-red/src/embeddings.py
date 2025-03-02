from transformers import AutoTokenizer, AutoModel
import torch
# pip install flash-attn transformers git+https://github.com/huggingface/transformers.git triton

# TinyLlama/TinyLlama-1.1B
MODEL = "meta-llama/Llama-3.1-8B"

from transformers import AutoModelForCausalLM, AutoTokenizer

class EmbeddingHandler:

    def __init__(self):
        self.model = AutoTokenizer.from_pretrained(MODEL)
        self.model.eval()

    def tokenize(self, text):
        inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True
                )
        # Use GPU if available
        if torch.cuda.is_available():
            self.model.to('cuda')
            inputs = {k: v.to('cuda') for k, v in inputs.items()}
            
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()

        return {
            'embeddings': embeddings,
        }
