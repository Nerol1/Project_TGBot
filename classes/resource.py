from aiogram.types import FSInputFile

import os

from .enums import ResourcePath, Extensions


class Button:
    def __init__(self, path: str, name=None):
        self._path = os.path.join(ResourcePath.PROMPTS.value, path + Extensions.TXT.value)
        if name:
            self.name = name
        else:
            with open(self._path, 'r', encoding='UTF-8') as txt_file:
                self.name = txt_file.readline().split(', ')[0][5:]
        self.callback = path


class Buttons:
    def __init__(self):
        self.buttons = self._read_buttons()

    @staticmethod
    def _read_buttons() -> list[Button]:
        buttons_list = [file for file in os.listdir(ResourcePath.PROMPTS.value) if file.startswith('talk_')]
        buttons = [Button(file.split('.')[0]) for file in buttons_list]
        return buttons

    def __iter__(self):
        return self

    def __next__(self):
        while self.buttons:
            return self.buttons.pop(0)
        raise StopIteration


class Resource:

    def __init__(self, file_name: str):
        self._file_name = file_name

    @property
    def photo(self):
        photo_path = os.path.join(ResourcePath.IMAGES.value, self._file_name + Extensions.JPG.value)
        if os.path.exists(photo_path):
            return FSInputFile(photo_path)

    @property
    def text(self):
        text_path = os.path.join(ResourcePath.MESSAGES.value, self._file_name + Extensions.TXT.value)
        if os.path.exists(text_path):
            with open(text_path, 'r', encoding='UTF-8') as file:
                return file.read()

    def as_kwargs(self) -> dict[str, FSInputFile | str]:
        return {'photo': self.photo, 'caption': self.text}