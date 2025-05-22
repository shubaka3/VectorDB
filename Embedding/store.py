class MemoryStore:
    def __init__(self):
        self._store = {}  # id -> text

    def add(self, text_list):
        for idx, text in enumerate(text_list):
            self._store[idx] = text

    def get(self, idx):
        return self._store.get(idx, None)

    def all(self):
        return self._store
