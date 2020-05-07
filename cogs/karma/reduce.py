from discord.ext import commands
from discord.ext.commands import has_any_role

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService


from util.config import roles


# Karma Reducer Class remove karma
class KarmaReducer(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._karma_service = KarmaService()

    # remove all karma from member
    @has_any_role(roles()['admin'], roles()['moderator'])
    @commands.command(brief='Reset all karma of a member, requires admin or moderator',
                      description='prefix reset member_id')
    async def reset(self, ctx, member):
        guild_id: str = str(ctx.message.guild.id)
        self._karma_service.delete_all_karma(KarmaMember(guild_id, member))
        await ctx.channel.send('Removed all Karma from {}'.format(member))


class KarmaBlocker(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._karma_service = KarmaService()

    async def blacklist(self, ctx, member):
        guild_id: str = str(ctx.message.guild.id)
        await ctx.channel.send('Blacklisted {}'.format(member))

    async def whitelist(self, ctx, member):
        guild_id: str = str(ctx.message.guild.id)
        await ctx.channel.send('Whitelisted {}'.format(member))
