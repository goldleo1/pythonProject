import sys
import typing

def isFloat(abc:str):
    assert type(abc) == str
    return abc.count('.') == 1 and sum(map(lambda x:x.isdigit(),abc.split('.')))==2

class ArgParser:
    def __init__(self) -> None:
        self.keys = list()
        self.types = dict()
        self.result = dict()

    def isFloat(self, abc:str):
        assert type(abc) == str
        return abc.count('.') == 1 and sum(map(lambda x:x.isdigit(),abc.split('.')))==2

        
    def _isKey(self, key:str):
        if key.startswith('-'):
            if key[1:] in self.keys:
                return True
            else:
                raise Exception('invaild key {}, this key is not registered'.format(key[1:]))
        else:
            return False

    def _toKeys(self, keyStr):
        return keyStr[1:]

    def setAnything(self, key):
        self.types[key] = typing.Any
        self.keys.append(key)
    def setOption(self, key):
        self.types[key] = True
        self.keys.append(key)
    def setBool(self, key):
        self.types[key] = bool
        self.keys.append(key)
    def setInt(self, key):
        self.types[key] = int
        self.keys.append(key)
    def setStr(self, key):
        self.types[key] = int
        self.keys.append(key)
    def setFloat(self, key):
        self.types[key] = float
        self.keys.append(key)

    def parse(self, key, idx, argv=sys.argv):
        if self.types[key] == True:
            if not self._isKey(argv[idx+1]):
                self.result[key] = True
                return False
            else:
                raise Exception('Value is not required')
        elif self.types[key] == typing.Any:
            if not self._isKey(argv[idx+1]):
                self.result[key] = argv[idx+1]
            else:
                raise Exception('Need a value : Any')
        elif self.types[key] == int:
            if not self._isKey(argv[idx+1]):
                if argv[idx+1].isdigit():
                    self.result[key] = int(argv[idx+1])
                else:
                    raise Exception('Unexpected type {} - int required'.format(type(argv[idx+1])))
            else:
                raise Exception('Need a value : int')
        elif self.types[key] == float:
            if not self._isKey(argv[idx+1]):
                if self.isFloat(argv[idx+1]):
                    self.result[key] = float(argv[idx+1])
                else:
                    raise Exception('Unexpected type {} - float required'.format(type(argv[idx+1])))
            else:
                raise Exception('Need a value : float')
        elif self.types[key] == str:
            if not self._isKey(argv[idx+1]):
                self.result[key] = argv[idx+1]
            else:
                raise Exception('Need a value : str')
        return True
    
    def get(self, argv=sys.argv):
        l = len(argv)-1
        idx = 0
        while idx < l:
            if self._isKey(argv[idx]):
                key = self._toKeys(argv[idx])
                if self.parse(key, idx):
                    idx += 2
                else:
                    idx += 1
            else:
                idx += 1
        return self.result

if __name__ == '__main__':
    arg = ArgParser()
    arg.setAnything('key')
    arg.setInt('count')
    arg.setFloat('float')

    parsed = arg.get()
    print(parsed)