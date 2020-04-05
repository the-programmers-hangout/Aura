from collections import defaultdict

import discord
from discord.ext import commands
import yaml


class Karma(commands.Cog):
    def __init__(self, bot, karma_type):
        self.bot = bot
        self.karma_type = karma_type
        with open("config.yaml", 'r') as stream:
            self.config = yaml.safe_load(stream)

    karma_type: str

    @commands.command(name=karma_type)
    async def give_karma(self, ctx, member: discord.Member = None):
        # check if message has a mention
        if not member:
            await ctx.channel.send(str(self.config['default-messages']['no-mention'])
                                   .format(self.bot.prefix, self.karma_type))
        else:
            guild_id: int = int(self.config['guild'])
            guild = self.bot.get_guild(guild_id)
            message = ctx.message
            if guild.get_member(message.author.id).mentioned_in(message):
                await ctx.channel.send(str(self.config['default-messages']['self'])
                                       .format(message.author.mention))
            elif self.bot.get_user(self.bot.user.id).mentioned_in(message):
                await ctx.channel.send(str(self.config['default-messages']['bot'])
                                       .format(message.author.mention))
            else:
                if guild.get_member(member).mentioned_in(message):
                    await ctx.channel.send(str(self.config['default-messages']['gain'])
                                           .format(member.mention, self.karma_type))

    async def update_karma(self, helper_id: int):
        print('db check')

    async def cooldown_user(self, giver_id: int):
        print('db check')