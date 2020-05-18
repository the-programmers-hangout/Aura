import logging

from discord.ext import commands
from discord.ext.commands import has_any_role, has_role, guild_only

from core import datasource
from core.model.member import KarmaMember, Member
from core.service.karma_service import KarmaService, BlockerService

from util.config import roles, config

log = logging.getLogger(__name__)


# Karma Reducer Class remove karma
class KarmaReducer(commands.Cog):

    def __init__(self, bot, karma_service=KarmaService(datasource.karma)):
        self.bot = bot
        self.karma_service = karma_service

    # remove all karma from member
    @guild_only()
    @has_any_role(roles()['admin'], roles()['moderator'])
    @commands.command(brief='Reset all karma of a member in the guild',
                      usage='{}reset member_id\n{}reset <@!member_id>'
                      .format(config['prefix'], config['prefix']))
    async def reset(self, ctx, *, member_id):
        guild_id: int = ctx.message.guild.id
        if len(ctx.message.mentions) == 1:
            self.karma_service.delete_all_karma(KarmaMember(guild_id, ctx.message.mentions[0].id))
        else:
            self.karma_service.delete_all_karma(KarmaMember(guild_id, member_id))
        await ctx.channel.send('Removed all Karma from {}'.format(member_id))


class KarmaBlocker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.blocker_service = BlockerService(datasource.blacklist)

    @guild_only()
    @has_role(roles()['admin'])
    @commands.command(brief='blacklists a member from giving karma',
                      usage='{}blacklist member_id\n{}blacklist <@!member_id>'
                      .format(config['prefix'], config['prefix']))
    async def blacklist(self, ctx, member):
        if len(ctx.message.mentions) == 1:
            self.blocker_service.blacklist(Member(ctx.message.guild.id, ctx.message.mentions[0].id))
        else:
            self.blocker_service.blacklist(Member(ctx.message.guild.id, member))
        await ctx.channel.send('Blacklisted {}'.format(member))

    @guild_only()
    @has_role(roles()['admin'])
    @commands.command(brief='removes existing blacklist of the guild member',
                      usage='{}whitelist member_id\n{}whitelist <@!member_id>'
                      .format(config['prefix'], config['prefix']))
    async def whitelist(self, ctx, *, member):
        if len(ctx.message.mentions) == 1:
            self.blocker_service.whitelist(Member(ctx.message.guild.id, ctx.message.mentions[0].id))
        else:
            self.blocker_service.whitelist(Member(ctx.message.guild.id, member))
        await ctx.channel.send('Whitelisted {}'.format(member))
