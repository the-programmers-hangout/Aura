import logging

from discord.ext import commands
from discord.ext.commands import has_any_role, has_role, guild_only

from core import datasource
from core.model.member import KarmaMember, Member
from core.service.karma_service import KarmaService, BlockerService

from util.config import roles, config
from util.conversion import convert_content_to_member_list

log = logging.getLogger(__name__)


class KarmaReducer(commands.Cog):

    def __init__(self, bot, karma_service=KarmaService(datasource.karma)):
        self.bot = bot
        self.karma_service = karma_service

    @guild_only()
    @has_any_role(roles()['admin'], roles()['moderator'])
    @commands.command(brief='Reset all karma of a member in the guild',
                      usage='{}reset member_id\n{}reset <@!member_id>'
                      .format(config['prefix'], config['prefix']))
    async def reset(self, ctx, *, args=''):
        member_list = await convert_content_to_member_list(ctx, args.split())
        for member in member_list:
            self.karma_service.delete_karma_member(KarmaMember(ctx.guild.id, member.id))
            await ctx.channel.send('Removed all Karma from {}'.format(member.mention))


class KarmaBlocker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.blocker_service = BlockerService(datasource.blacklist)

    @guild_only()
    @has_any_role(roles()['admin'], roles()['moderator'])
    @commands.command(brief='blacklists a member from giving karma',
                      usage='{}blacklist member_id\n{}blacklist <@!member_id>'
                      .format(config['prefix'], config['prefix']))
    async def blacklist(self, ctx, *, args):
        member_list = await convert_content_to_member_list(ctx, args.split())
        for member in member_list:
            self.blocker_service.blacklist(Member(ctx.guild.id, member.id))
            await ctx.channel.send('Blacklisted {}'.format(member.mention))

    @guild_only()
    @has_any_role(roles()['admin'], roles()['moderator'])
    @commands.command(brief='removes existing blacklist of the guild member',
                      usage='{}whitelist member_id\n{}whitelist <@!member_id>'
                      .format(config['prefix'], config['prefix']))
    async def whitelist(self, ctx, *, args):
        member_list = await convert_content_to_member_list(ctx, args.split())
        for member in member_list:
            self.blocker_service.whitelist(Member(ctx.guild.id, member.id))
            await ctx.channel.send('Whitelisted {}'.format(member.mention))

