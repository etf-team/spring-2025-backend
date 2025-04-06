class Registry[T]:
    def __init__(self):
        self._list = []

    def register(self, o: T) -> None:
        self._list.append(o)

    def get_all(self) -> list[T]:
        return self._list
