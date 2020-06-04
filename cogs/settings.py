import logging
from collections import Mapping

from discord import Embed
from discord.ext import commands
from discord.ext.commands import has_role, guild_only

from util.config import config, write_config, roles, descriptions
from util.constants import embed_color
from util.embedutil import add_filler_fields

log = logging.getLogger(__name__)


class SettingsManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # edit config defined in config.yaml, return messages if incorrect args are provided.
    # no checks on non existing configuration
    @guild_only()
    @has_role(roles()['admin'])
    @commands.command(brief='configuration menu or configuration modification',
                      usage='{}config\n{}config [keys] [new_value]\n{}config help [keys]'
                      .format(config['prefix'], config['prefix'], config['prefix']))
    async def config(self, ctx, *, params: str = ""):
        args = params.split()
        if len(args) >= 2 and args[0] == 'karma' and args[1] == 'keywords':
            keywords = params.replace('karma keywords', '')
            args[2] = keywords.strip()
            args = args[:3]
        if len(args) > 3:
            await ctx.channel.send('You provided too many arguments to the config command')
        else:
            if len(args) == 0:
                embed = self.build_config_embed()
                await ctx.channel.send(embed=embed)
            else:
                if args[0] == 'help':
                    embed = self.build_config_help_embed(args)
                    await ctx.channel.send(embed=embed)
                elif args[0] != 'token' and args[0] != 'prefix' \
                        and args[0] != 'database' and args[0] != 'logging':
                    if len(args) == 3 and config[args[0]] is not None:
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
                                    description='Shows all changeable configuration keys '
                                                + 'and their current values ',
                                    colour=embed_color)
        for key in config.keys():
            if key != 'token' and key != 'prefix' and key != 'database' and key != 'logging':
                if isinstance(config[key], Mapping):
                    for other_key in config[key].keys():
                        config_embed.add_field(name=f'**{key} {other_key}**', value=config[key][other_key])
                else:
                    config_embed.add_field(name=f'**{key}**', value=config[key])
        config_embed = add_filler_fields(config_embed, config_embed.fields)
        config_embed.set_footer(text='token, prefix, database, logging level only only changeable before runtime')
        return config_embed

    def build_config_help_embed(self, args) -> Embed:
        config_help_embed: Embed = Embed(colour=embed_color)
        # args[0] == help
        if len(args) == 2:
            config_help_embed.title = args[1]
            config_description = descriptions[args[1]]
            config_help_embed.description = config_description.description
            config_help_embed.add_field(name='Possible Values',
                                        value=self.build_possible_values(config_description.values))
        else:
            config_help_embed.title = args[1] + ' ' + args[2]
            config_description = descriptions[args[1]][args[2]]
            config_help_embed.description = config_description.description
            config_help_embed.add_field(name='Possible Values',
                                        value=self.build_possible_values(config_description.values))
        return config_help_embed

    def build_possible_values(self, value_list):
        result = ''
        if len(value_list) > 1:
            for value in value_list:
                result += value + ", "
            result = result[:-2]
        else:
            result = value_list[0]
        return result
