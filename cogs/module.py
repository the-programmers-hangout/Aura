import logging

from discord.ext import commands
from discord.ext.commands import has_role

from util.config import roles
from util.constants import cog_mapping

log = logging.getLogger(__name__)


# based on https://github.com/Rapptz/RoboDanny/blob/master/cogs/admin.py#L18
class ModuleManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @has_role(roles()['admin'])
    @commands.command()
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        try:
            self.bot.add_cog(cog_mapping[module])
        except Exception as e:
            log.error('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send(f'Loaded module {module}')

    @has_role(roles()['admin'])
    @commands.command()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        try:
            self.bot.remove_cog(module)
        except Exception as e:
            log.error('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send(f'Unloaded module {module}')

    @has_role(roles()['admin'])
    @commands.command(name='reload')
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        try:
            self.bot.remove_cog(module)
            self.bot.add_cog(cog_mapping[module])
        except Exception as e:
            log.error('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send(f'Reloaded module {module}')
