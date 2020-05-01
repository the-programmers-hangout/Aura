from discord.ext import commands
from discord.ext.commands import has_any_role

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService
from util.config import ConfigStore


# Karma Manager Class, reset member karma or blacklist them.
class KarmaManager(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._configManager = ConfigStore()
        self._config = self._configManager.config
        self._karma_service = KarmaService()

    # remove all karma from member
    @has_any_role(ConfigStore().roles['admin'], ConfigStore().roles['moderator'])
    @commands.command()
    async def reset(self, ctx, member_id):
        guild_id: str = self._config['guild']
        self._karma_service.delete_all_karma(KarmaMember(guild_id, member_id))
        await ctx.channel.send('Removed all Karma from {}'.format(member_id))
