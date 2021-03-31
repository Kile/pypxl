Using this code:

```py
from pypxl import Pxlapi
import discord
from discord.ext import commands
import io

bot = commands.Bot(command_prefix= commands.when_mentioned_or('pxl.'), description="Testing pxlapi wrapper", case_insensitive=True)

pxl = Pxlapi(token="pxlapi-token", stop_on_error=False)

@bot.command()
async def glitch(ctx, url:str):
    data = await pxl.glitch(images=[url])
    if isinstance(data, str):
        return await ctx.send(':x: '+data)
    f = discord.File(io.BytesIO(data), filename="test.gif")
    await ctx.send(file=f)


bot.run("bot-token")
```
We just created a simple `pxl.glitch` command! By setting `stop_on_error` to `False` the function will instead of raising an error if something goes wwrong, return the error text.
This is useful as we don't have handle the error and can just reply to the user what they did wrong.
