from discord.ext import commands

from util.config import config, write_config


class SettingsManager(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")

    # edit config defined in config.yaml, return messages if incorrect args are provided.
    # no checks on non existing configuration
    @commands.command()
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
