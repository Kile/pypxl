# pypxl
An asynchronous wrapper for pxlapi

# How to use it
```py
from pypxl import Pxlapi
#Define yout details here
pxl = Pxlapi(token="Your pxlapi token", stop_on_error=False)
```

Now you can use a all pxlapi features with just one line of code!
```py
glitch = await pxl.glitch(images=["https://cdn.discordapp.com/avatars/606162661184372736/a_62245605493deac02c291fe8fa517bee.gif?size=512"])
```

# Docs
I have not written any documentation. Generally every enpoint has a function with the same name and the same parameters as the enpoint along with the same default values. For an example in a discord bot, please look [here](https://github.com/Kile/pypxl/blob/main/examples/glitch_discord.markdown)

For questions and suggestions, join my discord server or dm me (`Kile#0606`)

 <a> [![Discord Server](https://img.shields.io/discord/691713541262147687.svg?label=Discord&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2&style=flat)](https://discord.gg/zXqDHkm)
</a>
