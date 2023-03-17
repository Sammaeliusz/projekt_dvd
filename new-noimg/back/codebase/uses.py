

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
