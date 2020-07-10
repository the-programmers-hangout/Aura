import logging
from io import BytesIO

from discord import File
from discord.ext import commands
from discord.ext.commands import has_any_role, guild_only

from core import datasource
from core.decorator import has_required_role
from core.model.member import KarmaMember, Member
from core.service.karma_service import KarmaMemberService, BlockerService
from util.config import roles, config, max_message_length
from util.conversion import convert_content_to_member_set
from util.util import member_has_role

log = logging.getLogger(__name__)


class KarmaReducer(commands.Cog):
    # Class all about reducing the Karma of a Member
    def __init__(self, bot, karma_service=KarmaMemberService(datasource.karma)):
        self.bot = bot
        self.karma_service = karma_service

    @guild_only()
    @has_any_role(roles()["admin"], roles()["moderator"])
    @commands.command(
        brief="Reset all karma of a member in the guild", usage="{}reset member_id\n{}reset <@!member_id>".format(config["prefix"], config["prefix"])
    )
    async def reset(self, ctx, *, args: str) -> None:
        """
        reset karma of the users provided to the command, both mentions and ids are valid.
        :param ctx: context of the invocation
        :param args: members provided to reset karma
        :return: None
        """
        # convert args to discord.Member
        member_set = await convert_content_to_member_set(ctx, args.split())
        for member in member_set:
            if member_has_role(member, roles()["admin"]) and ctx.message.author.id != int(config["owner"]):
                await ctx.channel.send("You cannot reset the karma of an admin.")
            else:
                if member_has_role(member, roles()["moderator"]) and not member_has_role(ctx.message.author, roles()["admin"]):
                    await ctx.channel.send("Only admins can reset the karma of an moderator.")
                else:
                    self.karma_service.delete_all_karma(KarmaMember(ctx.guild.id, member.id))
                    await ctx.channel.send("Removed all Karma from {}".format(member.mention))


class KarmaBlocker(commands.Cog):
    # Class about blocking and unblocking members from giving karma
    def __init__(self, bot):
        self.bot = bot
        self.blocker_service = BlockerService(datasource.blacklist)

    @guild_only()
    @has_required_role(command_name="blacklist")
    @commands.command(
        brief="blacklists a member from giving karma",
        usage="{}blacklist member_id\n{}blacklist <@!member_id>".format(config["prefix"], config["prefix"]),
    )
    async def blacklist(self, ctx, *, args: str) -> None:
        """
        blacklist the users provided to the command, both mentions and ids are valid.
        :param ctx: context of the invocation
        :param args: members provided to blacklist
        :return: None
        """
        member_set = await convert_content_to_member_set(ctx, args.split())
        for member in member_set:
            if member_has_role(member, roles()["admin"]) and ctx.message.author.id != int(config["owner"]):
                await ctx.channel.send("You cannot blacklist an admin.")
            else:
                if member_has_role(member, roles()["moderator"]) and not member_has_role(ctx.message.author, roles()["admin"]):
                    await ctx.channel.send("Only admins can blacklist an moderator.")
                else:
                    self.blocker_service.blacklist(Member(ctx.guild.id, member.id))
                    await ctx.channel.send("Blacklisted {}".format(member.mention))

    @guild_only()
    @has_required_role(command_name="whitelist")
    @commands.command(
        brief="removes existing blacklist of the guild member",
        usage="{}whitelist member_id\n{}whitelist <@!member_id>".format(config["prefix"], config["prefix"]),
    )
    async def whitelist(self, ctx, *, args: str) -> None:
        """
        whitelist the users provided to the command, both mentions and ids are valid.
        :param ctx: context of the invocation
        :param args: members provided to whitelist
        :return: None
        """
        member_set = await convert_content_to_member_set(ctx, args.split())
        for member in member_set:
            if member_has_role(member, roles()["admin"]) and ctx.message.author.id != int(config["owner"]):
                await ctx.channel.send("You cannot whitelist an admin.")
            else:
                if member_has_role(member, roles()["moderator"]) and not member_has_role(ctx.message.author, roles()["admin"]):
                    await ctx.channel.send("Only admins can whitelist an moderator.")
                else:
                    self.blocker_service.whitelist(Member(ctx.guild.id, member.id))
                    await ctx.channel.send("Whitelisted {}".format(member.mention))

    @guild_only()
    @has_required_role(command_name="showblacklist")
    @commands.command(
        name="showblacklist",
        brief="list all blacklisted members in the guild the command was invoked in",
        usage="{}showblackist".format(config["prefix"]),
    )
    async def show_blacklist(self, ctx) -> None:
        """
        prints out the blacklist in the channel, if message is over a certain max size the blacklist is embedded
        into a text file.
        :param ctx: context of the invocation
        :return: None
        """
        blacklist = list(self.blocker_service.find_all_blacklisted(str(ctx.guild.id)))
        return_message = ""
        for blacklisted in blacklist:
            member = ctx.guild.get_member(int(blacklisted["member_id"]))
            if member is not None:
                return_message += member.name + "#" + member.discriminator + " :: " + str(member.id) + "\n"
            else:
                return_message += return_message + str(blacklisted["member_id"]) + "\n"
        if len(return_message) != 0:
            if len(return_message) <= max_message_length:
                await ctx.channel.send(return_message)
            else:
                await ctx.channel.send(file=File(fp=BytesIO(bytes(return_message, "utf-8")), filename="Blacklist"))
        else:
            await ctx.channel.send("Blacklist is empty")
