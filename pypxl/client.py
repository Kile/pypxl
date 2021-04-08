import aiohttp
import json
from errors import PxlapiException, InvalidFlag, TooManyCharacters, InvalidSafety, InvalidEyes

class Pxlapi():


    def __init__(self, token:str, session=aiohttp.ClientSession(), stop_on_error:bool=False):
        self.token = token
        self.session = session
        self.stop_on_error = stop_on_error

        self.flags = ["asexual", "aromantic", "bisexual", "pansexual", "gay", "lesbian", "trans", "nonbinary", "genderfluid", "genderqueer", "polysexual", "austria", "belgium", "botswana", "bulgaria", "ivory", "estonia", "france", "gabon", "gambia", "germany", "guinea", "hungary", "indonesia", "ireland", "italy", "luxembourg", "monaco", "nigeria", "poland", "russia", "romania", "sierraleone", "thailand", "ukraine", "yemen"]
        self.filters = ["dog", "dog2", "dog3", "pig", "flowers", "random"] 
        self.safe_search = ["off", "moderate", "strict"]
        self.valid_eyes = ["big", "black", "bloodshot", "blue", "default", "googly", "green", "horror", "illuminati", "money", "pink", "red", "small", "spinner", "spongebob", "white", "yellow", "random"]

    async def get_img(self, enpoint:str, body:dict):
        session = aiohttp.ClientSession() 
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Application {self.token}'
        } 

        async with session.post(f'https://api.pxlapi.dev/{enpoint}', headers=headers, json=body) as r: 
            if r.status == 200:
                image_bytes = await r.read()
                await session.close()
                return image_bytes
            else:
                await session.close()
                error = str(await r.text())

                if self.stop_on_error:
                    raise PxlapiException(error)
                return error

    async def get_text(self, enpoint:str, body:dict):
        session = aiohttp.ClientSession()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Application {self.token}'
        } 

        async with session.post(f'https://api.pxlapi.dev/{enpoint}', headers=headers, json=body) as r: 
            if r.status == 200:
                data = await r.json()
                await session.close()
                return data
            else:
                await session.close()
                error = str(await r.text())
                
                if self.stop_on_error:
                    raise PxlapiException(error)
                return error


    async def emojaic(self, images:list, groupSize:int=12, scale:bool=False):
        body = {
            'images': images, 
            'groupSize': groupSize,
            'scale': scale
        } 
        
        return await self.get_img('emojimosaic', body)


    async def flag(self, flag:str, images:str, opacity:int=128):
        if not flag.lower() in self.flags:
            if self.stop_on_error:
                raise InvalidFlag(f'Flag {flag.lower()} not a valid flag')
            else:
                return f'Flag {flag.lower()} not a valid flag'

        body = {
            'images': images,
            'opacity': opacity,
        }
        return await self.get_img(f'flag/{flag.lower()}', body)


    async def glitch(self, images:list, delay:int=100, count:int=10, amount:int=5, iterations:int=10):
        body = {
            'images': images,
            'delay': delay,
            'count': count,
            'amount': amount,
            'iterations': iterations
        }
        return await self.get_img('glitch', body)


    async def lego(self, images:list, scale:bool=False, groupSize:int=8):
        body = {
            'images': images,
            'scale': scale,
            'groupSize': groupSize
        }
        return await self.get_img('lego', body)


    async def snapchat(self, filter:str, images:list, filters:list=None):
        if not filter.lower() in self.filters:
            if self.stop_on_error:
                raise InvalidFilter(f'Flag {filter.lower()} not a valid filter')
            else:
                return f'Flag {filter.lower()} not a valid filter'

        body = {
            'images': images,
            'filters': filters
        }
        return await self.get_img(f'snapchat/{filter}', body)

    async def eyes(self, eyes:str, images:list, filters:list=None):
        if not eyes.lower() in self.valid_eyes:
            if self.stop_on_error:
                raise InvalidEyes(f'Flag {eyes.lower()} not a valid eye type')
            else:
                return f'Flag {eyes.lower()} not a valid eye type'

        body = {
            'images': images,
            'filters': filters
        }
        return await self.get_img(f'eyes/{eyes}', body)

    async def thonkify(self, text:str):
        body = {
            'text': text
        }
        return await self.get_img('thonkify', body)

    async def sonic(self, text:str):
        if len(text) > 1000:
            if self.stop_on_error:
                raise TooManyCharacters("Too many characters used for the sonic endpoint")
            else:
                return "Too many characters used for the sonic endpoint"

        body = {
            'text': text
        }
        return await self.get_img('sonic', body)

    async def jpeg(self, images:list, quality:int=1):
        body = {
            'images': images,
            'quality': quality
        }
        return await self.get_img('jpeg', body)

    async def image_search(self, query:str, safeSearch:str='strict', meta:bool=False):
        if len(query) > 128:
            if self.stop_on_error:
                raise TooManyCharacters("Too many characters used for the image_search endpoint")
            else:
                return "Too many characters used for the image_search endpoint"
        if not safeSearch.lower() in self.safe_search:
            if self.stop_on_error:
                raise InvalidSafety("Invalid safety level for the image_search endpoint")
            else:
                return "Invalid safety level for the image_search endpoint"

        body = {
            'query': query,
            'safeSearch': safeSearch,
            'meta': meta
        }
        return await self.get_text('image_search', body)

    async def screenshot(self, url:str, device:str=None, locale:str='en_US', blocklist:list=[], defaultBlocklist:bool=True, browser:str='chromium', theme:str='dark', timeout:int=30000):
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
        return await self.get_img('screenshot', body)

    async def web_search(self, query:str, safeSearch:str='strict'):
        if len(query) > 128:
            if self.stop_on_error:
                raise TooManyCharacters("Too many characters used for the web_search endpoint")
            else:
                return "Too many characters used for the web_search endpoint"
        if not safeSearch.lower() in self.safe_search:
            if self.stop_on_error:
                raise InvalidSafety("Invalid safety level for the web_search endpoint")
            else:
                return "Invalid safety level for the web_search endpoint"

        body = {
            'query': query,
            'safeSearch': safeSearch
        }
        return await self.get_text('web_search', body)
