import logging

import discord
from discord.ext import commands
from discord.ext.commands import guild_only

from core import datasource
from core.decorator import has_required_role
from core.model.member import KarmaMember
from core.service.karma_service import KarmaMemberService
from util.config import profile, config
from util.constants import embed_color, bold_field
from util.conversion import convert_content_to_member_set
from util.embedutil import add_filler_fields

log = logging.getLogger(__name__)


class KarmaProfile(commands.Cog):
    # Karma Profile Class, users other than moderators and admins can only see their own karma or profile.
    # Moderators and Admin Role Users can get the karma by issuing the command with the user id.

    def __init__(self, bot, karma_service=KarmaMemberService(datasource.karma)):
        self.bot = bot
        self.karma_service = karma_service

    @guild_only()
    @has_required_role(command_name="karma")
    @commands.command(
        brief="get karma of a user, of several users or yourself",
        usage="{}karma\n{}karma <@!member_id> [...]".format(config["prefix"], config["prefix"]),
    )
    async def karma(self, ctx, *, args="") -> None:
        """
        Return the karma of all members provided to the karma command or self if no arguments.
        :param ctx: context of the invocation
        :param args: members to print the karma in the channel
        :return: None
        """
        return_msg = ""
        if len(args) == 0:
            karma_member = KarmaMember(ctx.guild.id, ctx.message.author.id)
            karma = self.karma_service.aggregate_member_by_karma(karma_member)
            if karma is None:
                return_msg += "{} has earned a total of {} karma\n".format(ctx.message.author.name + "#" + ctx.message.author.discriminator, 0)
            else:
                return_msg += "{} has earned a total of {} karma".format(ctx.message.author.name + "#" + ctx.message.author.discriminator, karma)
        else:
            member_set = await convert_content_to_member_set(ctx, args.split())
            for member in member_set:
                karma_member = KarmaMember(ctx.guild.id, member.id)
                karma = self.karma_service.aggregate_member_by_karma(karma_member)
                if karma is None:
                    return_msg += "{} has earned a total of {} karma\n".format(member.name + "#" + member.discriminator, 0)
                else:
                    return_msg += "{} has earned a total of {} karma\n".format(member.name + "#" + member.discriminator, karma)
        await ctx.channel.send(return_msg)

    @guild_only()
    @has_required_role(command_name="profile")
    @commands.command(
        brief="get karma profile of a user or yourself", usage="{}profile\n{}profile <@!member_id>".format(config["prefix"], config["prefix"])
    )
    async def profile(self, ctx, *, args="") -> None:
        """
        Return the karma profile of a member or self if no arguments.
        :param ctx: context of the invocation
        :param args: args provided to profile command, only take the first one.
        :return: None
        """
        if len(args) == 0:
            karma_member = KarmaMember(ctx.guild.id, ctx.message.author.id)
            embed = await self.build_profile_embed(karma_member, ctx.guild)
            if ctx.message.author.nick is None:
                embed.title = "Profile of {}".format(ctx.message.author.name + "#" + ctx.message.author.discriminator)
            else:
                embed.title = "Profile of {}".format(ctx.message.author.nick)
            embed.set_thumbnail(url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)
        else:
            member_list = args.split()
            member_id = member_list[0]
            member_set = await convert_content_to_member_set(ctx, [member_id])
            for member in member_set:
                karma_member = KarmaMember(ctx.guild.id, member.id)
                embed = await self.build_profile_embed(karma_member, ctx.guild)
                if member.nick is None:
                    embed.title = "Profile of {}".format(member.name + "#" + member.discriminator)
                else:
                    embed.title = "Profile of {}".format(member.nick)
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.channel.send(embed=embed)

    async def build_profile_embed(self, karma_member: KarmaMember, guild: discord.Guild) -> discord.Embed:
        """
        Build the profile embed with top channel breakdown configured
        :param karma_member: member whose profile to show
        :param guild: the discord guild
        :return: discord.Embed
        """
        channel_cursor = self.karma_service.aggregate_member_by_channels(karma_member)
        embed: discord.Embed = discord.Embed(colour=embed_color)
        embed.description = "Karma Profile with breakdown of top {} channels".format(profile()["channels"])
        channel_list = list(channel_cursor)
        total_karma = self.karma_service.aggregate_member_by_karma(karma_member)
        if len(channel_list) > 0:
            embed.add_field(name="0", value="0", inline=False)
            index = 0
            for document in channel_list:
                channel = guild.get_channel(int(document["_id"]["channel_id"]))
                if (index % 3) == 0 and index != 0:
                    if channel is None:
                        embed.add_field(name=bold_field.format("deleted channel"), value=document["karma"], inline=False)
                    else:
                        embed.add_field(name=bold_field.format(channel.name), value=document["karma"], inline=False)
                else:
                    if channel is None:
                        embed.add_field(name=bold_field.format("deleted channel"), value=document["karma"], inline=True)
                    else:
                        embed.add_field(name=bold_field.format(channel.name), value=document["karma"], inline=True)

            embed = add_filler_fields(embed, channel_list)
            embed.set_field_at(index=0, name="**total**", value=str(total_karma), inline=False)
            return embed
        else:
            # small embed since no karma etc.
            embed.add_field(name="**total**", value="0", inline=False)
            return embed
