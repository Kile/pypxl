import aiohttp
import json
from .errors import PxlapiException, InvalidFlag, TooManyCharacters, InvalidSafety, InvalidEyes
from .pxl_object import PxlObject

from typing import List

class PxlClient:
    """
    The class which allows you to make requests to pxlapi

    # Parameters:
        `token (string)`: Your pxlapi token

    # Optional parameters:
        `session (aiohttp client session)`: The session to use for requests
        `stop_on_error (boolean)`: If the code should raise an error if something went wrong or return the error text instead
    """
    def __init__(self, token:str, session=aiohttp.ClientSession(), stop_on_error:bool=False) -> PxlObject:
        self.token = token
        self.session = session
        self.stop_on_error = stop_on_error

        self.flags = ["asexual", "aromantic", "bisexual", "pansexual", "gay", "lesbian", "trans", "nonbinary", "genderfluid", "genderqueer", "polysexual", "austria", "belgium", "botswana", "bulgaria", "ivory", "estonia", "france", "gabon", "gambia", "germany", "guinea", "hungary", "indonesia", "ireland", "italy", "luxembourg", "monaco", "nigeria", "poland", "russia", "romania", "sierraleone", "thailand", "ukraine", "yemen"]
        self.filters = ["dog", "dog2", "dog3", "pig", "flowers", "clown", "random"] 
        self.safe_search = ["off", "moderate", "strict"]
        self.valid_eyes = ["big", "black", "bloodshot", "blue", "default", "googly", "green", "horror", "illuminati", "money", "pink", "red", "small", "spinner", "spongebob", "white", "yellow", "random"]

    async def _get_img(self, enpoint:str, body:dict) -> PxlObject:
        """
        The function making the request which gets image bytes in return. Not meant to be used outside of this class

        # Parameters:
            `endpoint (string)`: The endpoint to make the request to
            `body (dictionary)`: The body of the request

        # Returns:
            `PxlObject`
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Application {self.token}'
        } 
        try:
            r = await self.session.post(f'https://api.pxlapi.dev/{enpoint}', headers=headers, json=body)
        except Exception as e:
            if self.stop_on_error:
                raise e
            return PxlObject(success=False, error=str(e))
        if r.status == 200:
            image_bytes = await r.read()
            return PxlObject(success=True, image_bytes=image_bytes, content_type=r.content_type)
        else:
            error = str(await r.text())

            if self.stop_on_error:
                raise PxlapiException(error)
            return PxlObject(success=False, error=error)

    async def _get_text(self, enpoint:str, body:dict) -> PxlObject:
        """
        The function making the request which gets text in return. Not meant to be used outside of this class

        # Parameters:
            `endpoint (string)`: The endpoint to make the request to
            `body (dictionary)`: The body of the request

        # Returns:
            `PxlObject`
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Application {self.token}'
        } 
        try:
            r = await self.session.post(f'https://api.pxlapi.dev/{enpoint}', headers=headers, json=body) 
        except Exception as e:
            if self.stop_on_error:
                raise e
            return PxlObject(success=False, error=str(e))
        if r.status == 200:
            data = await r.json()
            return PxlObject(data=data, success=True)
        else:
            error = str(await r.text())
            if self.stop_on_error:
                raise PxlapiException(error)

            return PxlObject(error=error, success=False)

    async def emojaic(self, images:List[str], groupSize:int=12, scale:bool=False) -> PxlObject:
        """
        Turns the provided images into images assebled by emojis

        # Parameters:
            `images (list)`: The images to proccess
            `groupSize (int)`: The group size
            `scale (boolean)`: To have the returned image at the same scale or not

        # Returns:
            `PxlObject`
        """
        body = {
            'images': images, 
            'groupSize': groupSize,
            'scale': scale
        } 
        
        return await self._get_img('emojimosaic', body)

    async def flag(self, flag:str, images:List[str], opacity:int=128) -> PxlObject:
        """
        Turns the provided images into images with the flag specified

        # Parameters:
            `images (list)`: The images to proccess
            `flag (string)`: The name of the flag to use
            `opacity (int)`: What opacity to overlay the flag with

        # Returns:
            `PxlObject`
        """
        if not flag.lower() in self.flags:
            if self.stop_on_error:
                raise InvalidFlag(f'Flag {flag.lower()} not a valid flag')
            else:
                return PxlObject(success=False, error=f'Flag {flag.lower()} not a valid flag')

        body = {
            'images': images,
            'opacity': opacity,
        }
        return await self._get_img(f'flag/{flag.lower()}', body)

    async def ganimal(self, images:List[str]) -> PxlObject:
        """
        Turns the provided images into images with animal faces

        # Parameters:
            `images (list)`: The images to proccess

        # Returns:
            `PxlObject`
        """
        body = {
            'images': images
        }
        return await self._get_img('ganimal', body)

    async def ajit(self, images:List[str]) -> PxlObject:
        """
        Overlays an image of Ajit Pai snacking on some popcorn

        # Parameters:
            `images (list)`: The images to proccess

        # Returns:
            `PxlObject`
        """
        body = {
            'images': images
        }
        return await self._get_img('ajit', body)

    async def flash(self, images:List[str]) -> PxlObject:
        """
        Turns the provided images into flash images

        # Parameters:
            `images (list)`: The images to proccess

        # Returns:
            `PxlObject`
        """
        body = {
            'images': images
        }
        return await self._get_img('flash', body)

    async def glitch(self, images:List[str], delay:int=100, count:int=10, amount:int=5, iterations:int=10, gif:bool=None) -> PxlObject:
        """
        Turns the provided images into images into glitch GIFs and/or images

        # Parameters:
            `images (list)`: The images to proccess
            `delay (int)`: How long to display each frame for (in ms)
            `count (int)`: How many frames to generate
            `amount (int)`: Byte chunk length
            `iterations (int)`: How many byte chunks to modify,
            `gif (boolean)`: Additional information for glitching static images into a GIF

        # Returns:
            `PxlObject`
        """
        body = {
            'images': images,
            'delay': delay,
            'count': count,
            'amount': amount,
            'iterations': iterations,
            'gif': gif
        }
        return await self._get_img('glitch', body)

    async def lego(self, images:List[str], scale:bool=False, groupSize:int=8) -> PxlObject:
        """
        Turns the provided images into images into images made up of lego bricks

        # Parameters:
            `images (list)`: The images to proccess
            `scale (boolean)`: Whether to resize the resulting image to the original images dimensions
            `groupSize (int)`: How big of a pixel square to group into one brick. Defaults to a 32x32 brick result

        # Returns:
            `PxlObject`
        """
        body = {
            'images': images,
            'scale': scale,
            'groupSize': groupSize
        }
        return await self._get_img('lego', body)
    
    async def jpeg(self, images:List[str], quality:int=1) -> PxlObject:
        """
        Turns the provided images into lower quality

        # Parameters:
            `images (list)`: The images to proccess
            `quality (int)`: What JPEG quality to encode the image as

        # Returns:
            `PxlObject`
        """
        body = {
            'images': images,
            'quality': quality
        }
        return await self._get_img('jpeg', body)

    async def snapchat(self, filter:str, images:List[str], filters:list=None) -> PxlObject:
        """
        Turns the provided images into images with the snap filter provided if a face is detected

        # Parameters:
            `images (list)`: The images to proccess
            `filter (string)`: The filter to apply
            `filters (list)`: What filters to limit "random" to (defaults to all available filters)

        # Returns:
            `PxlObject`
        """
        if not filter.lower() in self.filters:
            if self.stop_on_error:
                raise InvalidFilter(f'Flag {filter.lower()} not a valid filter')
            else:
                return PxlObject(success=False, error=f'Flag {filter.lower()} not a valid filter')

        body = {
            'images': images,
            'filters': filters
        }
        return await self._get_img(f'snapchat/{filter}', body)

    async def eyes(self, eyes:str, images:List[str], filters:list=None) -> PxlObject:
        """
        Turns the provided images into images with a filter applied to the eyes of faces detected

        # Parameters:
            `images (list)`: The images to proccess
            `eyes (string)`: The filter to apply
            `filters (list)`: What filters to limit "random" to (defaults to all available filters)

        # Returns:
            `PxlObject`
        """
        if not eyes.lower() in self.valid_eyes:
            if self.stop_on_error:
                raise InvalidEyes(f'Eye {eyes.lower()} not a valid eye type')
            else:
                return PxlObject(success=False, error=f'Eye {eyes.lower()} not a valid eye type')

        body = {
            'images': images,
            'filters': filters
        }
        return await self._get_img(f'eyes/{eyes}', body)

    async def thonkify(self, text:str) -> PxlObject:
        """
        Turns the provided text into an image with that text made up of thonks

        # Parameters:
            `text (string)`: The text to thonkify

        # Returns:
            `PxlObject`
        """
        body = {
            'text': text
        }
        return await self._get_img('thonkify', body)

    async def sonic(self, text:str) -> PxlObject:
        """
        Turns the provided text into an image with sonic saying the provided text

        # Parameters:
            `text (string)`: The text to let sonic say

        # Returns:
            `PxlObject`
        """
        if len(text) > 1000:
            if self.stop_on_error:
                raise TooManyCharacters("Too many characters used for the sonic endpoint")
            else:
                return PxlObject(success=False, error="Too many characters used for the sonic endpoint")

        body = {
            'text': text
        }
        return await self._get_img('sonic', body)

    async def klines(self, pair:str=None, interval:str="1m", limit:int=90, ticks:List[int]=None, custom:dict=None):
        """
        Creates a candlestick chart for the given coin pair / ticks

        # Parameters:
            `pair (string)`: The [coin pair](https://www.binance.com/api/v3/exchangeInfo) to generate a candlestick chart for (e.g. `BNBBUSD`). Optional if custom ticks are sent.
            `interval (string)`: Timespan between candlesticks
            `limit (int)`: How many candlesticks to draw
            `ticks (list)`: Custom ticks (lets you send in [binance API compatible](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data) tick data)
            `custom (dict)`: Custom pair data to display
                key `baseAsset (string)`: Custom base asset name to display
                value `quoteAsset (string)`: Custom quote asset name to display
        
        # Returns:
            `PxlObject`
        """
        body = {
            "interval": interval,
            "limit": limit,
            "ticks": ticks,
            "pair": pair,
        }
        return await self._get_img(f"klines{f'/{pair}' if pair else ''}", body)

    async def imagescript(self, version:str, code:str, inject=None, timeout:int=10000) -> PxlObject:
        """
        Evaluates code 

        # Parameters:
            `version (string)`: The version of imagescript to use
            `code (string)`: The code to evaluate
            `inject (object)`: The data to inject as global variables
            `timeout (int)`: Maximum run time in ms

        # Returns:
            `PxlObject`
        """
        body = {
            'code': code,
            'inject': inject,
            'timeout': timeout
        }
        return await self._get_img(f'imagescript/{version}', body)

    async def imagescript_version(self) -> PxlObject:
        """
        Gives you the available versions for imagescript

        # Parameters:
            None

        # Returns:
            `PxlObject`
        """
        body = {}
        return await self._get_text('imagescript/versions', body)

    async def image_search(self, query:str, safeSearch:str='strict', meta:bool=False) -> PxlObject:
        """
        Looks for images with provided query

        # Parameters:
            `query (string)`: What to search for
            `safeSearch (string)`: What safe search setting to use
            `meta (boolean)`: Whether to return meta data (page title and URL)

        # Returns:
            `PxlObject`
        """
        if len(query) > 128:
            if self.stop_on_error:
                raise TooManyCharacters("Too many characters used for the image_search endpoint")
            else:
                return PxlObject(success=False, error="Too many characters used for the image_search endpoint")
        if not safeSearch.lower() in self.safe_search:
            if self.stop_on_error:
                raise InvalidSafety("Invalid safety level for the image_search endpoint")
            else:
                return PxlObject(success=False, error="Invalid safety level for the image_search endpoint")

        body = {
            'query': query,
            'safeSearch': safeSearch,
            'meta': meta
        }
        return await self._get_text('image_search', body)

    async def screenshot(self, url:str, device:str=None, locale:str='en_US', blocklist:list=[], defaultBlocklist:bool=True, browser:str='chromium', theme:str='dark', timeout:int=30000, fullPage:bool=False) -> PxlObject:
        """
        Screenshots the webpage provided

        # Parameters:
            `url (string) -> PxlObject: The website to screenshot
            `device (string)`: The device to emulate. See [list of available devices](https://github.com/microsoft/playwright/blob/17e953c2d8bd19ace20059ffaaa85f3f23cfb19d/src/server/deviceDescriptors.js#L21-L857). Defaults to a non-specific browser with a viewport of 1920x1080 pixels.
            `locale (string)`: The locale to set the browser to
            `blocklist (list)`: A list of domains to block
            `defaultBlocklist (boolean)`: Whether to block a list of predefined, known-bad domains (e.g. NSFW content)
            `browser (string)`: What browser engine to use for screenshotting
            `theme (string)`: What theme to use
            `timout (int)`: The max time to wait until the site has loaded (in ms)
            `fullPage (boolean)`: Whether to capture the entire page

        # Returns:
            `PxlObject`
        """
        body = {
            'url': url,
            'device': device,
            'locale': locale,
            'blocklist': blocklist,
            'defaultBlocklist': defaultBlocklist,
            'browser': browser,
            'theme': theme,
            'timeout': timeout
        }
        return await self._get_img('screenshot', body)

    async def web_search(self, query:str, safeSearch:str='strict') -> PxlObject:
        """
        Searches for the querie provided

        # Parameters:
            `url (string) -> PxlObject: The website to screenshot
            `safeSearch (string)`: What safe search setting to use

        # Returns:
            `PxlObject`
        """
        if len(query) > 128:
            if self.stop_on_error:
                raise TooManyCharacters("Too many characters used for the web_search endpoint")
            else:
                return PxlObject(success=False, error="Too many characters used for the web_search endpoint")
        if not safeSearch.lower() in self.safe_search:
            if self.stop_on_error:
                raise InvalidSafety("Invalid safety level for the web_search endpoint")
            else:
                return PxlObject(success=False, error="Invalid safety level for the web_search endpoint")

        body = {
            'query': query,
            'safeSearch': safeSearch
        }
        return await self._get_text('web_search', body)