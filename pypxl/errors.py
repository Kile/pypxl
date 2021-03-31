class PxlapiException(Exception):
    pass

class InvalidFlag(PxlapiException):
    pass

class InvalidFilter(PxlapiException):
    pass

class TooManyCharacters(PxlapiException):
    pass

class InvalidSafety(PxlapiException):
    pass