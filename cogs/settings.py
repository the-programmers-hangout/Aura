import logging

from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import has_role, guild_only

from util.config import config, write_config, roles

log = logging.getLogger(__name__)


class SettingsManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # edit config defined in config.yaml, return messages if incorrect args are provided.
    # no checks on non existing configuration
    @guild_only()
    @has_role(roles()['admin'])
    @commands.command(brief='configuration panel or configuration modification',
                      usage='{}config\n{}config keys new_value'
                      .format(config['prefix'], config['prefix']))
    async def config(self, ctx, *, params: str = ""):
        args = params.split()
        if len(args) > 3:
            await ctx.channel.send('You cannot send a message with more than three arguments.')
        elif len(args) == 0:
            embed = self.build_config_embed()
            await ctx.channel.send(embed=embed)
        else:
            if config[args[0]] is not None and args[0] != 'token' and args[0] != 'prefix' \
                    and args[0] != 'database' and args[0] != 'logging':
                if len(args) == 3:
                    if config[args[0]][args[1]] is not None:
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
                                    description='Shows all possible configuration keys '
                                                + 'that can be changed on runtime and their possible ' +
                                                'config values',
                                    colour=Color.dark_gold())
        config_embed.add_field(name='**blacklist entity**', value='any string for contact dm')
        config_embed.add_field(name='**blacklist emote**', value='true, false')
        config_embed.add_field(name='**blacklist message**', value='true, false')
        config_embed.add_field(name='**channel log**', value='channel id')
        config_embed.add_field(name='**cooldown**', value='time in seconds')
        config_embed.add_field(name='**karma time-emote**', value='true, false')
        config_embed.add_field(name='**karma time-message**', value='true, false')
        config_embed.add_field(name='**karma emote**', value='true, false')
        config_embed.add_field(name='**karma log**', value='true, false')
        config_embed.add_field(name='**karma message**', value='true, false')
        config_embed.add_field(name='**profile channels**', value='number of channels in profile')
        config_embed.add_field(name='**roles admin**', value='name of admin role')
        config_embed.add_field(name='**roles moderator**', value='name of moderator role')
        config_embed.set_footer(text='token, prefix, database, logging level only only changeable before runtime')
        config_embed.set_thumbnail(url=self.bot.user.avatar_url)
        return config_embed
