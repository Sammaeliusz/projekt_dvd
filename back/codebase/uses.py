

class Struct:
    def __init__(self, args:dict):
        for key, value in args.items():
            if isinstance(key, (list, tuple)):
                setattr(self, key, [Struct(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, Struct(value) if isinstance(value, dict) else value)

    def __add__(self, args:dict):
        for key, value in args.items():
            if isinstance(key, (list, tuple)):
                setattr(self, key, [Struct(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, Struct(value) if isinstance(value, dict) else value)

    def __getattr__(self, attr):
        return "Error"

    def hasattr(self, attr):
        return True if attr in self.__dict__.keys() else False

class sqlAnswer:
    def __init__(self, data, base=False):
        self.data = [None]
        for i in data:
            if isinstance(data, list) and len(data) > 0:
                if isinstance(i, bool):
                    if data:
                        self.data = i[0]
                    else:
                        self.data = base
                elif isinstance(i, list) and len(data) > 0:
                    if self.data[0]==None:
                        self.data=[[y for y in x] for x in data]
                    else:
                        self.data.append([[y for y in x] for x in data])
                else:
                    if isinstance(i, tuple):
                        self.data=([x for x in i])
                    else:
                        self.data=([x for x in data])
            else:
                if data:
                    self.data = data
                else:
                    self.data = base

    def struct(self):
        return Struct({'data':self.data})

    def list(self):
        return self.data if isinstance(self.data, list) else [self.data]

    def getId(self) -> int:
        if isinstance(self.data, list):
            if isinstance(self.data[0], int) and not isinstance(self.data[0], tuple):
                return self.data[0]
            elif isinstance(self.data[0], list):
                if isinstance(self.data[0][0], int):
                    return self.data[0][0]
                else:
                    return -1
            else:
                return -1
        elif isinstance(self.data, int) and not isinstance(self.data[0], tuple):
            return self.data
        else:
            return -1

    def hasData(self) -> bool:
        if isinstance(self.data, bool):
            return self.data
        elif not isinstance(self.data, list):
            return True
        else:
            if isinstance(self.data[0], list):
                return len(self.data[0]) > 0
            else:
                return len(self.data) > 0

    def isInfo(self) -> bool:
        if isinstance(self.data, list):
            return isinstance(self.data[0], str)
        else:
            return False

    def getError(self) -> str:
        if self.isInfo():
            return self.data[0]

    def isUsefull(self) -> bool:
        return not self.isInfo() and self.hasData()

    def getBool(self) -> bool:
        if self.data[0]==1:
            return True
        else:
            return False
            
