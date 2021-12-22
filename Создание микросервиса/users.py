import json
from pathlib import Path


class JSONUsersStorage:

    def __init__(self, filename):
        self._filename = Path(filename).resolve()
        if not self._filename.is_file():
            self.clear()

    def __setitem__(self, key, value):
        users = self._load()
        users[key] = value
        self._dump(users)

    def __getitem__(self, key):
        return self._load()[key]

    def __delitem__(self, key):
        users = self._load()
        del users[key]
        self._dump(users)

    def __contains__(self, item):
        return item in self._load()

    def clear(self):
        self._dump({})

    def _dump(self, obj):
        with open(self._filename, 'w') as file:
            json.dump(obj, file)

    def _load(self):
        with open(self._filename) as file:
            return json.load(file)