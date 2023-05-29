from ..Error.error import Error, Info

class Answer:
    
    flags: str
    
    def __init__(self, data, base=None):
        if isinstance(data, list):
            self.data = self.__unlist__(data)
            self.flags = f"L:{len(data)}:0"
        elif isinstance(data, Error):
            self.data = data
            self.flags = f"E:{data.getCode()}:{data.getFlags()}"
        elif isinstance(data, Info):
            self.data = data
            self.flags = f"I:{data.getCode()}:{data.getFlags()}"
        else:
            if data:
                self.data = data
                self.flags = f"D:0:0"
            else:
                self.data = base
                self.flags = f"B:0:0"

    def __unlist__(self, l:list| tuple) -> list:
        if len(l) == 1:
            if isinstance(l[0], (list, tuple)):
                return self.__unlist__(l[0])
            elif isinstance(l[0], (Answer)):
                return self.__unlist__(l[0].getList())
            else:
                return l[0]
        elif len(l) > 1:
            for x, y in enumerate(l):
                if isinstance(l[x], (list, tuple)):
                    l[x] = self.__unlist__(y)
                elif isinstance(l[x], (Answer)):
                    l[x] = self.__unlist__(y.getList())
            return list(l)
        return None

    def getFlags(self) -> list:
        return self.flags.split(':')

    def getList(self) -> list:
        return self.data if isinstance(self.data, list) else [self.data] if not self.data == None else []

    def getSelf(self):
        return self.data

    def getId(self, l=None) -> int:
        if isinstance(l, (Error, Info)):
            return l.getCode()
        if not l:
            if isinstance(self.data, int):
                return self.data
            if not isinstance(self.data, list):
                return -1
            if not len(self.data) > 0:
                return -1
            if not isinstance(self.data[0], (int,list)):
                return -1
            if not isinstance(self.data[0], int):
                if not len(self.data[0]) > 0:
                    return -1
                return self.getId(l=self.data[0])
            return self.data[0]
        
        if not len(l) > 0:
            return -1
        if not isinstance(l[0], (int,list)):
            return -1
        if not isinstance(l[0], int):
            if not len(l[0]) > 0:
                return -1
            return self.getId(l=l[0])
        return l[0]

    def hasData(self) -> bool:
        return self.data != None

    def getType(self) -> str:
        return self.getFlags()[0]

    def isError(self) -> bool:
        return self.getFlags()[0]=='E'

    def isInfo(self) -> bool:
        return self.getFlags()[0]=='I'

    def getError(self) -> Error:
        if self.isError():
            return self.data
        return None

    def getInfo(self) -> Info:
        if self.isInfo():
            return self.data
        return None

    def getMessage(self) -> str:
        if self.isError() or self.isInfo():
            return self.data.getMessage()

    def isUsefull(self) -> bool:
        return not self.isError() and not self.isInfo() and self.hasData()

    def getBool(self) -> bool:
        if isinstance(self.data, bool):
            return self.data
        else:
            return True if self.isInfo() else False

    def getGen(self):
        for x in self.getList():
            yield x