from discord.ext import commands
from discord.ext.commands import has_any_role, has_role

from core import datasource
from core.model.member import KarmaMember, Member
from core.service.karma_service import KarmaService, BlockerService

from util.config import roles


# Karma Reducer Class remove karma
class KarmaReducer(commands.Cog):

    def __init__(self, bot, karma_service=KarmaService(datasource.karma)):
        self.bot = bot
        self.karma_service = karma_service

    # remove all karma from member
    @has_any_role(roles()['admin'], roles()['moderator'])
    @commands.command(brief='Reset all karma of a member, requires admin or moderator',
                      description='prefix reset member_id')
    async def reset(self, ctx, member):
        guild_id: str = str(ctx.message.guild.id)
        self.karma_service.delete_all_karma(KarmaMember(guild_id, member))
        await ctx.channel.send('Removed all Karma from {}'.format(member))


class KarmaBlocker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.blocker_service = BlockerService(datasource.blacklist)

    @has_role(roles()['admin'])
    @commands.command(brief='blacklists a member from this bot, requires admin',
                      description='prefix blacklist member')
    async def blacklist(self, ctx, member):
        if len(ctx.message.mentions) == 1:
            self.blocker_service.blacklist(Member(ctx.message.guild.id, ctx.message.mentions[0].id))
        else:
            self.blocker_service.blacklist(Member(ctx.message.guild.id, member))
        await ctx.channel.send('Blacklisted {}'.format(member))

    @has_role(roles()['admin'])
    @commands.command(brief='removes existing blacklists of a member from this bot, requires admin',
                      description='prefix whitelist member')
    async def whitelist(self, ctx, *, member):
        if len(ctx.message.mentions) == 1:
            self.blocker_service.whitelist(Member(ctx.message.guild.id, ctx.message.mentions[0].id))
        else:
            self.blocker_service.whitelist(Member(ctx.message.guild.id, member))
        await ctx.channel.send('Whitelisted {}'.format(member))
