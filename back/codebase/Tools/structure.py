class Struct:
    def __init__(self, args:dict):
        for key, value in args.items():
            if isinstance(key, (list, tuple)):
                setattr(self, key, [Struct(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, Struct(value) if isinstance(value, dict) else value)

    def __add__(self, arg):
        for key, value in arg.dict().items():
            if isinstance(key, (list, tuple)):
                setattr(self, key, [Struct(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, Struct(value) if isinstance(value, dict) else value)
        return self

    def __getattr__(self, attr):
        return "Error"

    def dict(self):
        return self.__dict__

    def hasattr(self, attr):
        return True if attr in self.__dict__.keys() else False
