def MessageCreator(code:int, message='', separator='_', typ='ERROR'):
    if typ=='ERROR':
        return Error(code, message=message, separator=separator)
    return Info(code, message=message, separator=separator)

class Error:

    __code: int
    __message: str
    __FlagSeparator: str
    __flags: str

    def __init__(self, code, message="", separator='_'):

        self.__code = code
        self.__message = message
        self.__FlagSeparator = separator
        self.__flags = f"{f'M{len(message)}{self.__FlagSeparator}' if message else ''}E"

    def getCode(self) -> bool:
        return self.__code

    def getMessage(self) -> str:
        return self.__message

    def getFlags(self) -> str:
        return self.__flags.split(self.__FlagSeparator)

    def getFlagSeparator(self) -> str:
        return self.__FlagSeparator

    def getType(self) -> str:
        return "ERROR"

class Info(Error):

    def __init__(self, code, message="", separator='_'):

        self.__code = code
        self.__message = message
        self.__FlagSeparator = separator
        self.__flags = f"{f'M{len(message)}{self.__FlagSeparator}' if message else ''}I"

    def getType(self) -> str:
        return "INFO"

    def getMessage(self) -> str:
        return self.__message

