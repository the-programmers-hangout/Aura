import logging

import discord
from discord.ext import commands
from discord.ext.commands import guild_only, TextChannelConverter, CommandError

from core import datasource
from core.decorator import has_required_role
from core.service.karma_service import KarmaMemberService
from util.config import config
from util.constants import embed_color, bold_field, leaderboard_usage

log = logging.getLogger(__name__)


class KarmaLeaderboard(commands.Cog):
    # Karma Leaderboard classes
    def __init__(self, bot, karma_service=KarmaMemberService(datasource.karma)):
        self.bot = bot
        self.karma_service = karma_service

    @guild_only()
    @has_required_role(command_name="leaderboard")
    @commands.command(
        brief="get a global karma leaderboard or a channel leaderboard, " + "optionally you can provide days as an argument",
        usage=leaderboard_usage.format(config["prefix"], config["prefix"], config["prefix"], config["prefix"]),
    )
    async def leaderboard(self, ctx, channel_mention="", time_span: int = 0) -> None:
        """
        Leaderboard showing the top x users globally, channel specific and optionally of the last x days.
        :param ctx: context of the invocation
        :param channel_mention: optional channel mention for channel leaderboard
        :param time_span: time_span in days for the last x days leaderboard
        :return: None
        """
        embed = discord.Embed(colour=embed_color)
        guild = ctx.message.guild
        if channel_mention == "" or channel_mention == "global":
            if time_span == 0:
                leaderboard = list(self.karma_service.aggregate_top_karma_members(str(guild.id)))
                limit = config["leaderboard"]
                embed.title = f"Top {limit} most helpful people"
                if len(leaderboard) > 0:
                    count: int = 1
                    for document in leaderboard:
                        member = self.bot.get_user(int(document["_id"]["member_id"]))
                        karma = document["karma"]
                        if member is not None:
                            embed.add_field(
                                name=f"{count}) " + bold_field.format(member.name + "#" + member.discriminator), value=f"{karma} karma", inline=False
                            )
                        else:
                            embed.add_field(name=f"{count}) " + bold_field.format("deleted user"), value=f"{karma} karma", inline=False)
                        count += 1
                await ctx.channel.send(embed=embed)
            else:
                leaderboard = list(self.karma_service.aggregate_top_karma_members(guild_id=str(guild.id), time_span=time_span))
                limit = config["leaderboard"]
                embed.title = f"Top {limit} most helpful people of the last {time_span} days"
                if len(leaderboard) > 0:
                    count: int = 1
                    for document in leaderboard:
                        member = self.bot.get_user(int(document["_id"]["member_id"]))
                        karma = document["karma"]
                        if member is not None:
                            embed.add_field(
                                name=f"{count}) " + bold_field.format(member.name + "#" + member.discriminator), value=f"{karma} karma", inline=False
                            )
                        else:
                            embed.add_field(name=f"{count}) " + bold_field.format("deleted user"), value=f"{karma} karma", inline=False)
                        count += 1
                    await ctx.channel.send(embed=embed)
                else:
                    await ctx.channel.send("No leaderboard exists for this timeframe")
        else:
            input_channel = None
            input_channel_name = ""
            try:
                input_channel = await TextChannelConverter().convert(ctx=ctx, argument=channel_mention)
                input_channel_name = input_channel.name
            except CommandError as e:
                log.error(e)
            if input_channel is None:
                await ctx.channel.send("Channel does not exist or lacking permissions to view it.")
            else:
                if not ctx.message.author.permissions_in(input_channel).view_channel:
                    await ctx.channel.send("Channel does not exist or lacking permissions to view it.")
                else:
                    if time_span == 0:
                        leaderboard = list(self.karma_service.aggregate_top_karma_members(str(guild.id), str(input_channel.id)))
                        limit = config["leaderboard"]
                        embed.title = f"Top {limit} most helpful people in {input_channel_name}"
                        if len(leaderboard) > 0:
                            count: int = 1
                            for document in leaderboard:
                                member = self.bot.get_user(int(document["_id"]["member_id"]))
                                karma = document["karma"]
                                if member is not None:
                                    embed.add_field(
                                        name=f"{count}) " + bold_field.format(member.name + "#" + member.discriminator),
                                        value=f"{karma} karma",
                                        inline=False,
                                    )
                                else:
                                    embed.add_field(name=f"{count}) " + bold_field.format("deleted user"), value=f"{karma} karma", inline=False)
                                count += 1
                            await ctx.channel.send(embed=embed)
                        else:
                            await ctx.channel.send("No leaderboard exists for this channel.")
                    else:
                        leaderboard = list(
                            self.karma_service.aggregate_top_karma_members(
                                guild_id=str(guild.id), channel_id=str(input_channel.id), time_span=time_span
                            )
                        )
                        limit = config["leaderboard"]
                        embed.title = f"Top {limit} most helpful people in {input_channel_name} " f"of the last {time_span} days"
                        if len(leaderboard) > 0:
                            count: int = 1
                            for document in leaderboard:
                                member = self.bot.get_user(int(document["_id"]["member_id"]))
                                karma = document["karma"]
                                if member is not None:
                                    embed.add_field(
                                        name=f"{count}) " + bold_field.format(member.name + "#" + member.discriminator),
                                        value=f"{karma} karma",
                                        inline=False,
                                    )
                                else:
                                    embed.add_field(name=f"{count}) " + bold_field.format("deleted user"), value=f"{karma} karma", inline=False)
                                count += 1
                            await ctx.channel.send(embed=embed)
                        else:
                            await ctx.channel.send("No leaderboard exists for this timeframe")
