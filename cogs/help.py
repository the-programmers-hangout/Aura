import datetime
import logging
import time

from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import guild_only, CommandError

from util.config import config, author_discord, version, repository
from util.conversion import strfdelta

log = logging.getLogger(__name__)


class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @guild_only()
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message) and len(message.content) == len('<@!{}>'.format(self.bot.user.id)):
            embed: Embed = Embed()
            embed.title = self.bot.user.name + "#" + self.bot.user.discriminator
            embed.description = 'A bot for handling karma points.'
            embed.add_field(name='Prefix', value=config['prefix'], inline=True)
            embed.add_field(name='Contributors', value=author_discord(), inline=True)
            version_field = '```\nVersion: {}\ndiscord.py: {}\npython: {}```' \
                .format(version()['aura_version'], version()['discord_version'], version()['python_version'])
            embed.add_field(name='Build Info', value=version_field, inline=False)
            current_time = time.time()
            difference = int(round(current_time - self.start_time))
            uptime = datetime.timedelta(seconds=difference)
            embed.add_field(name='Uptime',
                            value=strfdelta(uptime, '{hours} hours, {minutes} minutes, {seconds} seconds'),
                            inline=False)
            embed.add_field(name='Source', value=repository(), inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await self.bot.get_channel(message.channel.id).send(embed=embed)

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
                embed.add_field(name='**' + 'Structure' + '**', value=command.usage)
            else:
                embed.title = 'Error: Command not found'
                embed.description = 'Command does not exist or you do not have the permissions to view it'
        return embed
