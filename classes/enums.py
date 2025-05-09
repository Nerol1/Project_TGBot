import os
from enum import Enum


class ResourcePath(Enum):
    RESOURCES = 'resources'
    IMAGES = os.path.join(RESOURCES, 'images')
    MESSAGES = os.path.join(RESOURCES, 'messages')
    PROMPTS = os.path.join(RESOURCES, 'prompts')


class GPTRole(Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class Extensions(Enum):
    JPG = '.jpg'
    TXT = '.txt'

class Languages(Enum):
    RU = 'Русский язык'
    EN = 'Английский язык'
    DE = 'Немецкий язык'
    ZH = 'Китайский язык'
    FR = 'Французский язык'
    AR = 'Арабский язык'