# pypxl
An asynchronous wrapper for [pxlapi](https://pxlapi.dev)

# Install it
Just use `pip3 install pypxl` to install it

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
I have not written any documentation. Generally every enpoint has a function with the same name and the same parameters as the enpoint along with the same default values. For an example in a discord bot, please click [here](https://github.com/Kile/pypxl/blob/main/examples/glitch_discord.markdown)

I have implemented all functions this library offers in commands in my bot. You can find all those commands [here](https://github.com/Kile/Killua/blob/main/killua/cogs/pxlapi.py)

For questions and suggestions, join my discord server or dm me (`Kile#0606`)

 <a> [![Discord Server](https://img.shields.io/discord/691713541262147687.svg?label=Discord&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2&style=flat)](https://discord.gg/zXqDHkm)
</a>
