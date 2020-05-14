import logging

import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import guild_only

from core import datasource
from core.model.member import KarmaMember
from core.service.karma_service import KarmaService

# Karma Profile Class, users other than moderators and admins can only see their own karma or profile.
# Moderators and Admin Role Users can get the karma by issuing the command with the user id.
from util.config import profile

log = logging.getLogger(__name__)


class KarmaProfile(commands.Cog):

    def __init__(self, bot, karma_service=KarmaService(datasource.karma)):
        self.bot = bot
        self.karma_service = karma_service

    # get karma of yourself without any arguments, get karma of others with mention
    @guild_only()
    @commands.command(brief='get karma of users or yourself',
                      description='prefix karma or prefix karma user_mention')
    async def karma(self, ctx):
        guild_id: str = str(ctx.message.guild.id)
        message = ctx.message
        return_msg = ''
        if len(message.mentions) > 0:
            for member in message.mentions:
                karma_member = KarmaMember(guild_id, member.id)
                karma = self.karma_service.aggregate_member_by_karma(karma_member)
                if karma is None:
                    return_msg += '{} has earned a total of {} karma\n'.format(member.name + '#' + member.discriminator,
                                                                               0)
                else:
                    return_msg += '{} has earned a total of {} karma\n'.format(member.name + '#' + member.discriminator,
                                                                               karma)
        elif len(message.mentions) == 0:
            karma_member = KarmaMember(guild_id, ctx.message.author.id)
            karma = self.karma_service.aggregate_member_by_karma(karma_member)
            if karma is None:
                return_msg += '{} has earned a total of {} karma\n'.format(ctx.message.author.name + '#'
                                                                           + ctx.message.author.discriminator, 0)
            else:
                return_msg += '{} has earned a total of {} karma'.format(ctx.message.author.name + '#'
                                                                         + ctx.message.author.discriminator, karma)
        await ctx.channel.send(return_msg)

    @guild_only()
    @commands.command(brief='get karma profile of a user or yourself',
                      description='prefix profile or prefix profile user_mention')
    async def profile(self, ctx):
        guild_id: str = str(ctx.message.guild.id)
        guild = self.bot.get_guild(int(guild_id))
        if len(ctx.message.mentions) == 0:
            karma_member = KarmaMember(guild_id, ctx.message.author.id)
            embed = await self.build_profile_embed(karma_member, guild)
            if ctx.message.author.nick is None:
                embed.title = "Profile of {}".format(ctx.message.author.name + "#" + ctx.message.author.discriminator)
            else:
                embed.title = "Profile of {}".format(ctx.message.author.nick)
            embed.set_thumbnail(url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)
        elif len(ctx.message.mentions) == 1:
            message = ctx.message
            member = message.mentions[0]
            if not self.bot.get_user(self.bot.user.id).mentioned_in(message) and guild.get_member(
                    member.id).mentioned_in(message):
                karma_member = KarmaMember(guild_id, member.id)
                embed = await self.build_profile_embed(karma_member, guild)
                if member.nick is None:
                    embed.title = "Profile of {}".format(member.name + "#" + member.discriminator)
                else:
                    embed.title = "Profile of {}".format(member.nick)
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.channel.send(embed=embed)

    async def build_profile_embed(self, karma_member: KarmaMember, guild) -> discord.Embed:
        channel_cursor = self.karma_service.aggregate_member_by_channels(karma_member)
        embed: discord.Embed = discord.Embed(colour=Color.dark_gold())
        embed.description = 'Karma Profile with breakdown of top {} channels'.format(profile()['channels'])
        total_karma: int = 0
        channel_list = list(channel_cursor)
        if len(channel_list) > 0:
            embed.add_field(name='0', value='0', inline=False)
            index = 0
            for document in channel_list:
                total_karma += document['karma']
                channel = guild.get_channel(int(document['_id']['channel_id']))
                if (index % 3) == 0 and index != 0:
                    embed.add_field(name="**{}**".format(channel.name), value=document['karma'], inline=False)
                else:
                    embed.add_field(name="**{}**".format(channel.name), value=document['karma'], inline=True)
            if len(channel_list) % 3 != 0:
                embed.add_field(name='\u200b', value='\u200b')
            embed.set_field_at(index=0, name="**total**", value=str(total_karma), inline=False)
            return embed
        else:
            # small embed since no karma etc.
            embed.add_field(name="**total**", value=str(total_karma), inline=False)
            return embed
