from langchain_core.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage


class ChatMessageHistoryBuilder:

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.history = ChatMessageHistory()

    def add_user_message(self, question: str):
        self.history.add_user_message(f'\n\nQuestion: {question}')

    def add_assistant_message(self, answer: str):
        self.history.add_ai_message(answer)

    def get_recent_messages(self, max_turns: int = 4):
        return self.history.messages[-max_turns * 2 :]

    def build_prompt(self, retrieved_context: str, question: str) -> str:
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.system_prompt),
                MessagesPlaceholder(variable_name='history'),
                HumanMessage(
                    content=f'Document Excerpt:\n{retrieved_context}\n\nQuestion: {question}'
                ),
            ]
        )
        prompt = chat_prompt_template.invoke(
            {
                'history': self.get_recent_messages(),
                'question': question,
            }
        )
        return self._convert_to_llama_format(prompt.messages)

    format_instruction = """Answer in this exact format:\n"According to the document, [direct answer citing specific requirements]."
    
    Direct Answer:
    """

    def _convert_to_llama_format(self, messages: list[BaseMessage]):
        rendered = '<|begin_of_text|>'
        for msg in messages:
            role = msg.type
            header = {
                'system': 'system',
                'human': 'user',
                'ai': 'assistant',
            }.get(role)
            content = msg.content.strip()
            rendered += (
                f'<|start_header_id|>{header}<|end_header_id|>{content}<|eot_id|>'
            )
        rendered += '<|start_header_id|>assistant<|end_header_id|>'
        return rendered
