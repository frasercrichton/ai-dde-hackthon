# from fuzzywuzzy import fuzz
import torch
from src.tokenizer import Tokenizer
from src.chat_message_history_builder import ChatMessageHistoryBuilder
import re
from transformers import AutoModelForCausalLM

torch.cuda.empty_cache()
class LLM:

    LLAMA_MODEL = 'meta-llama/Llama-3.1-8B'

    def __init__(self, model_name: str, token: str):
        self.model_name = model_name

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            token=HF_TOKEN,
            device_map='auto' if device == 'cuda' else None,
            torch_dtype=torch.float16,
            max_memory={0: '38GiB'}  # if 40GB available, leave headroom
        ).to(device)
        self.model.eval()
        self.tokenizer = Tokenizer(self.model_name, token=HF_TOKEN)

    def run_prompt(self, prompt):
        
        inputs = self.tokenizer.tokenize(prompt, max_length=1024)
        input_length = inputs['input_ids'].shape[1]

        if torch.cuda.is_available():
            logger.info('Using GPU.')
            self.model.to('cuda')
            inputs = {k: v.to('cuda') for k, v in inputs.items()}

        # TODO - increase the token limit to allow for more text
        eos_token_id = self.tokenizer.eos_token_id or self.tokenizer.convert_tokens_to_ids('<|end_of_text|>')

        generation_config = {
          'max_new_tokens': 500,
          'eos_token_id': eos_token_id,
          'no_repeat_ngram_size': 3,
          'repetition_penalty': 1.2,
          'pad_token_id': eos_token_id,
          'do_sample': False, # ensures the model stays strictly factual and consistent with the source material plus it always returns the consistency of the reponse.
          # 'num_beams': 3,  # Small beam width for better answers
          # temperature=0.3,
          # do_sample=True,

    #       'temperature': 0.0,
    # 'top_p': 1.0,
    # 'top_k': 50,
        }

        with torch.no_grad():
            outputs = self.model.generate(
              **inputs,
              **generation_config
            )
            new_tokens = outputs[0, input_length:]
            response = self.tokenizer.decode(new_tokens).strip()
            print(f'answer {response}')
            print(f'------')
        return response



# class LLM:

#     def __init__(self, model_name: str):
#         self.model_name = model_name
#         self.model = None 

# # titles_list = [doc_metadata['title'] for doc_metadata in metadata_list.values()]

#     # TODO - if the chat bot doesn't recognise any keywords it should prompt back and say something like:
#     #  'Ask me about digital evidence related to photographic, video or etc. evidence.'
#     def ask_question_llama(self, question, case_law):
#         titles_list = []
#         metadata_titles = [titles_list[0]]
#         if case_law:
#             metadata_titles.append(titles_list[1])
#             extracted_keywords = extract_keywords(question)

#         metadata_keywords = find_keywords(extracted_keywords, keywords_list)
#         # metadata_titles = find_full_title(question, titles_list)
#         '''Generate an answer to a legal question using LLaMA.'''
#         # Get relevant documents
#         relevant_docs = processor.find_relevant_documents(query=question, metadata_keywords=metadata_keywords, metadata_titles=metadata_titles, n_results=5)


#         context_pieces = [doc['text'][4000:5000] for doc in relevant_docs]
#         titles = [doc['metadata']['title'] for doc in relevant_docs]
#         keywords = [doc['metadata']['keywords'] for doc in relevant_docs]
#         context = '\n'.join(context_pieces)

#         full_prompt = f'''You are a Human Rights Lawyer using the documents below to answer the following question.

#     Based on the documents above, provide a clear, concise answer. If relevant, refer to legal precedent, case law, or any specific details from the documents. Do not simply restate the question; make sure the answer is grounded in the provided content.

#     Use the context below to answer the question clearly and factually.

#     {context}
    
#     Question: {question}

#     Answer:'''

#     # EmbeddingHandler = EmbeddingsProcessor('sentence-transformers/all-MiniLM-L6-v2')

#         if torch.cuda.is_available():
#             self.model.to('cuda')
#         # TODO - increase the token limit to allow for more text
#         inputs = tokenizer(
#             full_prompt,
#             return_tensors='pt',
#             max_length=1024,
#             truncation=True
#         )
#         if torch.cuda.is_available():
#             inputs = {k: v.to('cuda') for k, v in inputs.items()}
#         # TODO - increase the token limit to allow for more text
#         with torch.no_grad():
#             outputs = self.model.generate(
#                 **inputs,
#                 max_new_tokens=800,
#                 temperature=0.7,
#                 do_sample=True
#             )
#         # Process output
#         # raw_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         # if 'Answer:' in raw_output:
#         #     final_answer = raw_output.split('Answer:', 1)[1].strip()
#         # else:
#         #     final_answer = raw_output

#         # docs = ',\n - '.join(metadata_titles)
#         # final_answer = final_answer + f'\n\n DOCUMENTS: {docs}' + '\n\n NOTE: this is only guidance based on past case law.'
#         # print(final_answer )
#         return outputs


#     # answer = ask_question_llama('Are you using the Leiden Guidelines and case law ?', True, True)
#     # print(answer)