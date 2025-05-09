from .chat_gpt import ChatGPT

gpt_client = ChatGPT()

__all__ = [
    'ChatGPT',
    'gpt_client',
]