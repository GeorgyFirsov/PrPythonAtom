import os
import pickle as pkl

class FileWriter:
    
    def __init__(self, path):
        if not self._check_path(path):
            os.system("touch " + path)
        self.path = path
        self.file = None
    
    def _check_path(self, path):
        try:
            f = open(path)
            f.close()
            return 1
        except:
            return 0
    
    def setPath(self, npath):
        self.path = npath

    def getPath(self):
        return self.path

    def delete(self):
        os.system("rm -rf " + self.path)

    def print_file(self):
        f = open(self.path)
        for ln in f:
            print(ln)
        f.close()
    
    def write(self, some_string):
        with open(self.path, 'a') as f:
            f.write(some_string)
    
    def save_yourself(self, file_name):
        with open(file_name, 'wb') as dumpFile:
            pkl.dump(self, dumpFile)
    
    @classmethod
    def load_file_writer(cls, pickle_file):
        with open(pickle_file, 'rb') as dumpFile:
            return pkl.load(dumpFile)

pt = 'fl.txt'

f = FileWriter(pt)
f.write("WORD1")
f.print_file()
f.save_yourself('d.pkl')
s = FileWriter.load_file_writer('d.pkl')
s.write("WORD2")
s.print_file()
