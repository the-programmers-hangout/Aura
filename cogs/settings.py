from discord.ext import commands
from discord.ext.commands import has_role

from util.config import ConfigStore


class SettingsManager(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")
        self._configManager = ConfigStore()
        self._config = self._configManager.config

    @has_role(ConfigStore().roles['admin'])
    @commands.command()
    async def config(self, ctx, *, params: str):
        args = params.split()
        if len(args) > 3:
            await ctx.channel.send('You cannot send a message with more than three arguments.')
        elif len(args) <= 1:
            await ctx.channel.send('Your message needs at least two arguments.')
        else:
            if len(args) == 3:
                self._config[args[0]][args[1]] = args[2]
                print(self._config[args[0]][args[1]])
                self._configManager.write_config()
                await ctx.channel.send(
                    'Configuration parameter {} {} has been changed to {}'.format(args[0], args[1], args[2]))
            else:
                self._config[args[0]] = args[1]
                self._configManager.write_config()
                await ctx.channel.send('Configuration parameter {} has been changed to {}'.format(args[0], args[1]))
