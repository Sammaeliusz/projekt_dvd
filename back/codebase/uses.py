

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
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], bool):
                if data:
                    self.data = data[0][0]
                else:
                    self.data = base
            elif isinstance(data[0], list) and len(data) > 0:
                self.data = [[y for y in x] for x in data]
            else:
                if isinstance(data[0], tuple):
                    self.data = [x for x in data[0]]
                else:
                    self.data = [x for x in data]
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
            
