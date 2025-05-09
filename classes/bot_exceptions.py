
class AllTrainedException(IndexError):
    def __init__(self):
        super().__init__("Слов для тренировки больше нет!")
