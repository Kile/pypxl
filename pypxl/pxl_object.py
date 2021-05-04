import io
from .errors import InvalidBytes

class PxlObject():
    """
    An object you will get as a response to any request

    # Properties:
        image_bytes (bytes): The image bytes of the response
        data (string): The data of the response as a dictionary
        success (boolean): If the request was successfull or not
        error (string): The error message if the request was not successful
        file_type (string): The file ending of the returned image(s)
        content_type (string): The content type of the image(s) returned

    # Methods:
        `convert_to_ioBytes()`
            Converts the image bytes to ioBytes
    """
    def __init__(self, image_bytes:bytes=None, data:dict=None, success:bool=True, error:str=None, content_type:str=None):
        self.image_bytes = image_bytes
        self.success = success
        self.ok = self.success # Serves as alias
        self.error = error
        self.content_type = content_type
        self.file_type = self.content_type.split('/')[1] if self.content_type else None
        self.data = data

    def convert_to_ioBytes(self):
        if not self.success:
            raise InvalidBytes("Cannot convert a failed request to io bytes")
        if not self.image_bytes:
            raise InvalidBytes("This object contains no bytes")

        return io.BytesIO(self.image_bytes)


    