class Stack:
    def __init__(self):
        self.__storage = []

    def push(self, value):
        self.__storage.append(value)

    def get(self):
        # Не удаляет запись после получения пользователем
        return self.__storage[-1]
    
    def pop(self):
        self.__storage.pop()

    @property
    def size(self):
        return len(self.__storage)

    @property
    def is_empty(self):
        return not bool(self.size)
