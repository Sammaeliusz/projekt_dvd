

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
    def __init__(self, data:list, base=False):
        if isinstance(data, bool):
            self.data+=data
        elif len(data) == 1:
            if isinstance(data[0], (list, tuple)):
                self.data += self.__init__(list(data[0]), base=True)
            elif base:
                self.data += data[0]
            else:
                self.data += data
        elif len(data)>1:
            data = list(data)
            for x, y in enumerate(data):
                if isinstance(data[x], (list, tuple)):
                    data[x] = self.__init__(y, base=True)
            self.data =  data
        else:
            self.data=False
    def distable(self, data:list, re=False) -> list:
        if len(data) == 1:
            if isinstance(data[0], (list, tuple)):
                return distable(self, list(data[0]), base=True)
            elif re:
                return data[0]
            else:
                return data
        elif len(data)>1:
            data = list(data)
            for x, y in enumerate(data):
                if isinstance(data[x], (list, tuple)):
                    data[x] = distable(self, y, re=True)
            return data

    def struct(self):
        return Struct({'data':self.data})

    def list(self):
        print(self.data)
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
