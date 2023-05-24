def MessageCreator(code:int, message='', separator='_', typ='ERROR'):
    if typ=='ERROR':
        return Error(code, message=message, separator=separator)
    return Info(code, message=message, separator=separator)

class Error:

    code: int
    message: str
    FlagSeparator: str
    flags: str

    def __init__(self, code, message="", separator='_'):

        self.code = code
        self.message = message
        self.FlagSeparator = separator
        self.flags = f"{f'M{len(message)}{self.FlagSeparator}' if message else ''}E"

    def getCode(self) -> int:
        return self.code

    def getMessage(self) -> str:
        return self.message

    def getFlags(self) -> str:
        return self.flags.split(self.FlagSeparator)

    def getFlagSeparator(self) -> str:
        return self.FlagSeparator

    def getType(self) -> str:
        return "ERROR"

class Info(Error):

    def __init__(self, code, message="", separator='_'):

        self.code = code
        self.message = message
        self.FlagSeparator = separator
        self.flags = f"{f'M{len(message)}{self.FlagSeparator}' if message else ''}I"

    def getType(self) -> str:
        return "INFO"

    def getMessage(self) -> str:
        return self.message
    
    def getCode(self) -> int:
        return self.code

