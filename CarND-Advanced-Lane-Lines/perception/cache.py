import pickle
import os

from .save import chmod_rw_all


class Cache:
    def __init__(self, fname):
        self.fname = "pickle/" + fname

    def exists(self):
        return os.path.isfile(self.fname)

    def save(self, data):
        pickle.dump(data, open(self.fname, "w+b"))
        chmod_rw_all(self.fname)

    def load(self):
        data = pickle.load(open(self.fname, "r+b"))
        return data
