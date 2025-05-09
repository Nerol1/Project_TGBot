import openai

import os

from .enums import GPTRole, Extensions
from .resource import ResourcePath
from .bot_exceptions import AllTrainedException


class GPTMessage:

    def __init__(self, prompt: str):
        self.prompt_file = prompt + Extensions.TXT.value
        self.message_list = self._init_message()
        self.words_list = []

    def _init_message(self) -> list[dict[str, str]]:
        message = {
            'role': GPTRole.SYSTEM.value,
            'content': self._load_prompt(),
        }
        return [message]

    def _load_prompt(self) -> str:
        prompt_path = os.path.join(ResourcePath.PROMPTS.value, self.prompt_file)
        with open(prompt_path, 'r', encoding='UTF-8') as file:
            prompt = file.read()
        return prompt

    def update(self, role: GPTRole, message: str):
        message = {
            'role': role.value,
            'content': message,
        }
        self.message_list.append(message)

    def add_new_word(self, word: str):
        self.words_list.append(word)

    def get_next_word(self):
        if self.words_list:
            return self.words_list.pop()
        else:
            raise AllTrainedException()



class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model: str = 'gpt-3.5-turbo'):
        self._gpt_token = os.getenv('GPT_TOKEN')
        self._client = self._create_client()
        self._model = model

    def _create_client(self):
        gpt_client = openai.AsyncOpenAI(
            api_key=self._gpt_token,
        )
        return gpt_client

    async def request(self, messages: GPTMessage) -> str:
        response = await self._client.chat.completions.create(
            messages=messages.message_list,
            model=self._model,
        )
        return response.choices[0].message.content