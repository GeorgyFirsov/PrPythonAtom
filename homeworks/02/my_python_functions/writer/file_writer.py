import os
import pickle as pkl

###############################################################################
#
#   _path - путь до файла
#   file  - булева переменная (а есть ли вообще сам файл)
#
#   в случае отсутствия файла он создается в __init__, "контекстной записи" и сеттере path
#   в методах print_file и делетере path действий не производится
#
###############################################################################

class FileWriter:
    
    def __init__(self, path):
        if not self._check_path(path):
            os.system("touch " + path) # создание
        self._path = path
        self.file = True
    
    def _check_path(self, path):
        try:
            f = open(path)
            f.close()
            return 1
        except:
            return 0
    
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, npath):

        # проверка
        if self.file != False:
            self.file = False

        if not self._check_path(npath):
            os.system("touch " + npath) # создание
        self._path = npath
        self.file = True

    @path.deleter # удалятор
    def path(self):
        self.file = False
        self._path = None

    def print_file(self):

        # проверка
        
        if self._path == None and self.file == False:
            raise Exception("print_file(): there's no information")
        if self.file == False:
            if not self._check_path(self._path):
                return
        
        f = open(self._path)
        for ln in f:
            print(ln)
        f.close()

    def __enter__(self):
        if self._path == None:
            raise Exception("write(): there's no information")
        if not self._check_path(self._path):
            self.file = True
            os.system("touch " + self._path)

        self.open_file = open(self.path, 'a')
        return self.open_file

    def __exit__(self, *args):
        self.open_file.close()
        del self.open_file
    
    def save_yourself(self, file_name):
        with open(file_name, 'wb') as dumpFile:
            if self.file != False:
                self.file = False
            pkl.dump(self, dumpFile)
    
    @classmethod
    def load_file_writer(cls, pickle_file):
        with open(pickle_file, 'rb') as dumpFile:
            res = pkl.load(dumpFile)
            if res._path == None:
                raise Exception("load_file_writer(): there's no information")
            if not res._check_path(res._path):
                res.file = False
                return res
            res.file = True
            return res
