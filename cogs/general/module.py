import logging

from discord.ext import commands

from core.decorator import has_required_role
from util.config import config
from util.constants import cog_map

log = logging.getLogger(__name__)


# based on https://github.com/Rapptz/RoboDanny/blob/master/cogs/admin.py#L18
class ModuleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_required_role(command_name="load")
    @commands.command(
        brief="load a module, module names are listed in the help menu overview",
        usage="{}load".format(config["prefix"]),
    )
    async def load(self, ctx, *, module: str) -> None:
        """
        the module to load, classes with commands.Cog
        :param ctx: context of the invocation
        :param module: proper name of the cog class
        :return: None
        """
        if module.lower() == "help":
            await ctx.channel.send(f"The {module} can only be reloaded.")
        else:
            try:
                self.bot.add_cog(cog_map[module])
            except Exception as e:
                await ctx.channel.send(f"Module with the name {module} does not exist.")
                log.error("{}: {}".format(type(e).__name__, e))
            else:
                await ctx.channel.send(f"Loaded module {module}")

    @has_required_role(command_name="unload")
    @commands.command(
        brief="unload a module, module names are listed in the help menu overview",
        usage="{}unload".format(config["prefix"]),
    )
    async def unload(self, ctx, *, module: str) -> None:
        """
        the module to unload, classes with commands.Cog
        :param ctx: context of the invocation
        :param module: proper name of the cog class
        :return: None
        """
        if module.lower() == "help":
            await ctx.channel.send(f"The module {module} cannot be unloaded")
        else:
            try:
                self.bot.remove_cog(module)
            except Exception as e:
                await ctx.channel.send(f"Module with the name {module} does not exist.")
                log.error("{}: {}".format(type(e).__name__, e))
            else:
                await ctx.channel.send(f"Unloaded module {module}")

    @has_required_role(command_name="reload")
    @commands.command(
        name="reload",
        brief="reload a module, module names are listed in the help menu overview",
        usage="{}reload".format(config["prefix"]),
    )
    async def _reload(self, ctx, *, module: str) -> None:
        """
        the module to reload, classes with commands.Cog
        :param ctx: context of the invocation
        :param module: proper name of the cog class
        :return: None
        """
        try:
            self.bot.remove_cog(module)
            self.bot.add_cog(cog_map[module])
        except Exception as e:
            await ctx.channel.send(f"Module with the name {module} does not exist.")
            log.error("{}: {}".format(type(e).__name__, e))
        else:
            await ctx.channel.send(f"Reloaded module {module}")
