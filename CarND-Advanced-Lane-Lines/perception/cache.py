import pickle
import os

from .save import chmod_rw_all


class Cache:
    def __init__(self, filename):
        self.filename = "pickle/" + filename

    def exists(self):
        return os.path.isfile(self.filename)

    def save(self, data):
        pickle.dump(data, open(self.filename, "w+b"))
        chmod_rw_all(self.filename)

    def load(self):
        data = pickle.load(open(self.filename, "r+b"))
        return data
