from discord import Embed, Color
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
    async def config(self, ctx, *, params: str = ""):
        args = params.split()
        if len(args) > 3:
            await ctx.channel.send('You cannot send a message with more than three arguments.')
        elif len(args) == 0:
            embed = self.build_config_embed()
            await ctx.channel.send(embed=embed)
        else:
            if config[args[0]] is not None and args[0] != 'token' and args[0] != 'prefix':
                if len(args) == 3:
                    if config[args[0]][args[1]] is not None \
                            and args[0] != 'token' and args[0] != 'prefix':
                        config[args[0]][args[1]] = args[2]
                        write_config()
                        await ctx.channel.send(
                            'Configuration parameter {} {} has been changed to {}'.format(args[0], args[1],
                                                                                          args[2]))
                else:
                    config[args[0]] = args[1]
                    write_config()
                    await ctx.channel.send('Configuration parameter {} has been changed to {}'.format(args[0], args[1]))

    def build_config_embed(self) -> Embed():
        config_embed: Embed = Embed(title='Aura Configuration Panel',
                                    description='Shows all possible configuration parameters '
                                                + 'that can be changed on runtime and their expected ' +
                                                'config values',
                                    colour=Color.dark_gold())
        config_embed.add_field(name='**blacklist**', value='ex. Modmail (contact dm)')
        config_embed.add_field(name='**channel log**', value='ex. channel id to log to')
        config_embed.add_field(name='**cooldown**', value='ex. 30 (seconds)')
        config_embed.add_field(name='**karma time-emote**', value='true, false')
        config_embed.add_field(name='**karma time-message**', value='true, false')
        config_embed.add_field(name='**database host**', value='ex. mongo')
        config_embed.add_field(name='**database name**', value='ex. aura')
        config_embed.add_field(name='**database password**', value='ex. example')
        config_embed.add_field(name='**database port**', value='ex. 27017')
        config_embed.add_field(name='**database username**', value='ex. root')
        config_embed.add_field(name='**karma emote**', value='true, false')
        config_embed.add_field(name='**karma log**', value='true, false')
        config_embed.add_field(name='**karma message**', value='true, false')
        config_embed.add_field(name='**profile channels**', value='ex. 5 (top 5 channels)')
        config_embed.add_field(name='**roles admin**', value='ex. Admin')
        config_embed.add_field(name='**roles moderator**', value='ex. Staff')
        config_embed.set_footer(text='**token and prefix only changable before runtime**')
        config_embed.set_thumbnail(url=self.bot.user.avatar_url)
        return config_embed
