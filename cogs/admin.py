from discord.ext import commands
from discord.ext.commands import has_role

from util.config import roles


# Changed based on the example at https://github.com/Rapptz/RoboDanny/blob/master/cogs/admin.py#L18
class Admin(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(briefdescription="load a module",
                      description='load a module')
    @has_role(roles()['admin'])
    async def load(self, *, module: str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(briefdescription="unload a module",
                      description='unload a module')
    @has_role(roles()['admin'])
    async def unload(self, *, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(name='reload', briefdescription="reload a module",
                      description='reload a module')
    @has_role(roles()['admin'])
    async def _reload(self, *, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')
