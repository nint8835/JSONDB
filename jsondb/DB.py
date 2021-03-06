import os
import json

from .Selection import JSONDBSelection


class JSONDB(object):

    def __init__(self, filename):
        self._filename = filename

        if not os.path.isfile(filename):
            self._rows = []
            self.save()
        else:
            self.load()

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, i):
        return self._rows[i]

    def __iter__(self):
        for row in self._rows:
            yield row

    def __str__(self):
        return json.dumps(self._rows)

    def save(self):
        with open(self._filename, "w") as f:
            json.dump(self._rows, f)

    def load(self):
        with open(self._filename) as f:
            self._rows = json.load(f)

    def select(self, expression):
        indexes = []
        for index, row in enumerate(self._rows):
            if expression(row):
                indexes.append(index)
        return JSONDBSelection(indexes, self)

    def insert(self, **kwargs):
        self._rows.append(kwargs)
        self.save()

    def update_row(self, row_index, key, value):
        self._rows[row_index][key] = value

    def get_row(self, row_index):
        return self._rows[row_index]
