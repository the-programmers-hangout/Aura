from discord.ext import commands
from discord.ext.commands import has_role

from util.config import config, write_config, roles


class SettingsManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # edit config defined in config.yaml, return messages if incorrect args are provided.
    # no checks on non existing configuration
    @has_role(roles()['admin'])
    @commands.command(brief='change configuration parameters, requires admin',
                      description='change config params to new value, last value in params is new_value')
    async def config(self, ctx, *, params: str):
        args = params.split()
        if len(args) > 3:
            await ctx.channel.send('You cannot send a message with more than three arguments.')
        elif len(args) <= 1:
            await ctx.channel.send('Your message needs at least two arguments.')
        else:
            if len(args) == 3:
                config[args[0]][args[1]] = args[2]
                write_config()
                await ctx.channel.send('Configuration parameter {} {} has been changed to {}'.format(args[0], args[1],
                                                                                                     args[2]))
            else:
                config[args[0]] = args[1]
                write_config()
                await ctx.channel.send('Configuration parameter {} has been changed to {}'.format(args[0], args[1]))
