import logging

from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import has_role, guild_only

from util.config import config, write_config, roles, karma, profile, blacklist

log = logging.getLogger(__name__)


class SettingsManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # edit config defined in config.yaml, return messages if incorrect args are provided.
    # no checks on non existing configuration
    @guild_only()
    @has_role(roles()['admin'])
    @commands.command(brief='configuration menu or configuration modification',
                      usage='{}config\n{}config keys new_value'
                      .format(config['prefix'], config['prefix']))
    async def config(self, ctx, *, params: str = ""):
        args = params.split()
        if len(args) == 0:
            embed = self.build_config_embed()
            await ctx.channel.send(embed=embed)
        else:
            if config[args[0]] is not None:
                if args[0] == 'help':
                    embed = self.build_config_help_embed()
                    await ctx.channel.send(embed=embed)
                elif args[0] != 'token' and args[0] != 'prefix' \
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
                        await ctx.channel.send(
                            'Configuration parameter {} has been changed to {}'.format(args[0], args[1]))

    def build_config_embed(self) -> Embed:
        config_embed: Embed = Embed(title='Aura Configuration Menu',
                                    description='Shows all possible configuration keys '
                                                + 'and their current values ',
                                    colour=Color.dark_gold())
        config_embed.add_field(name='**blacklist contact**', value=blacklist()['contact'])
        config_embed.add_field(name='**blacklist emote**', value=blacklist()['emote'])
        config_embed.add_field(name='**blacklist dm**', value=blacklist()['dm'])
        config_embed.add_field(name='**channel log**', value=config['channel']['log'])
        config_embed.add_field(name='**cooldown**', value=config['cooldown'])
        config_embed.add_field(name='**karma keywords**', value=karma()['keywords'])
        config_embed.add_field(name='**karma time-emote**', value=karma()['time-emote'])
        config_embed.add_field(name='**karma time-message**', value=karma()['time-message'])
        config_embed.add_field(name='**karma emote**', value=karma()['emote'])
        config_embed.add_field(name='**karma log**', value=karma()['log'])
        config_embed.add_field(name='**karma message**', value=karma()['message'])
        config_embed.add_field(name='**profile channels**', value=profile()['channels'])
        config_embed.add_field(name='**roles admin**', value=roles()['admin'])
        config_embed.add_field(name='**roles moderator**', value=roles()['moderator'])
        config_embed.add_field(name='\u200b', value='\u200b')
        config_embed.set_footer(text='token, prefix, database, logging level only only changeable before runtime')
        return config_embed

    def build_config_help_embed(self) -> Embed:
        print()