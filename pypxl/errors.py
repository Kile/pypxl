class PxlapiException(Exception):
    """
    The base exception for anything related to pypxl
    """
    pass

class InvalidFlag(PxlapiException):
    pass

class InvalidFilter(PxlapiException):
    pass

class InvalidEyes(PxlapiException):
    pass

class TooManyCharacters(PxlapiException):
    pass

class InvalidSafety(PxlapiException):
    pass

class PxlObjectError(PxlapiException):
    """
    A class which all errors originating from using the PxlOnject come from
    """
    pass

class InvalidBytes(PxlObjectError):
    pass