from transformers import AutoTokenizer

# TinyLlama/TinyLlama-1.1B
# MODEL = 'meta-llama/Llama-3.1-8B'

from transformers import AutoTokenizer


class Tokenizer:

    def __init__(self, model, token=None):
        kwargs = {'use_auth_token': token} if token else {}
        self.tokenizer = AutoTokenizer.from_pretrained(model, **kwargs)

    @property
    def eos_token(self):
        return self.tokenizer.eos_token

    @property
    def eos_token_id(self):
        return self.tokenizer.eos_token_id

    def tokenize(self, text, max_length=None):
        kwargs = {'max_length': max_length} if max_length else {}
        defaults = {'truncation': True, 'return_tensors': 'pt'}

        return self.tokenizer(text, **{**defaults, **kwargs})

    def decode(self, outputs, skip_special_tokens=True):
        # OLD return self.tokenizer.decode(outputs[0], skip_special_tokens)
        return self.tokenizer.decode(outputs, skip_special_tokens)
