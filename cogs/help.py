import logging

from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import guild_only, has_any_role, CommandError

from util.config import roles, config

log = logging.getLogger(__name__)


class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @guild_only()
    @commands.command(brief='show all commands or show help text of a single command',
                      usage='{}help\n{}help command'.format(config['prefix'], config['prefix']))
    async def help(self, ctx, *, params: str = ""):
        args = params.split()
        log.info('Called help command with args: {}'.format(args))
        if len(args) <= 1:
            embed = await self.build_help_embed(ctx, args)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send('You passed too many arguments to the help command.')

    # build the help embed that is to be returned to the user
    async def build_help_embed(self, ctx, args) -> Embed:
        embed = Embed(colour=Color.dark_gold())
        if len(args) == 0:
            embed.title = 'Help Menu'
            embed.description = 'Use {}help <command> for more information'.format(config['prefix'])
            cog_mapping = self.bot.cogs
            not_rendered_counter = 0
            for cog in cog_mapping:
                command_list = cog_mapping[cog].get_commands()
                if len(command_list) > 0:
                    embed_val = ''
                    for command in command_list:
                        is_executable = False
                        try:
                            is_executable = await command.can_run(ctx)
                        except CommandError:
                            pass
                        if is_executable:
                            embed_val += command.name + '\n'
                    if embed_val != '':
                        embed.add_field(name='**' + cog + '**', value=embed_val, inline=True)
                else:
                    not_rendered_counter -= 1
            if (len(cog_mapping) - not_rendered_counter) % 3 != 0:
                embed.add_field(name='\u200b', value='\u200b')
            if (len(cog_mapping) - not_rendered_counter + 1) % 3 != 0:
                embed.add_field(name='\u200b', value='\u200b')
        else:
            command = self.bot.get_command(args[0])
            is_executable = False
            try:
                is_executable = await command.can_run(ctx)
            except CommandError:
                pass
            if command is not None and is_executable:
                embed.title = command.name
                embed.description = command.brief
                embed.add_field(name='**'+'Structure'+'**', value=command.usage)
            else:
                embed.title = 'Error: Command not found'
                embed.description = 'Command does not exist or you do not have the permissions to view it'
        return embed
