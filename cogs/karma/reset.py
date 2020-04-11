from discord.ext import commands
from discord.ext.commands import has_any_role

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService
from util.config import ConfigManager


class KarmaCleaner(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._configManager = ConfigManager()
        self._config = self._configManager.config
        self._karma_service = KarmaService()

    @has_any_role(ConfigManager().roles['admin'], ConfigManager().roles['moderator'])
    @commands.command()
    async def reset(self, ctx, member_id, karma_type):
        guild_id: str = self._config['guild']
        if karma_type == 'all':
            self._karma_service.delete_all_karma(guild_id, str(member_id))
            await ctx.channel.send('Removed all Karma from {}'.format(member_id))
        elif karma_type in self._configManager.karma_categories:
            self._karma_service.delete_karma(KarmaMember(guild_id, member_id, karma_type))
            await ctx.channel.send('Removed all Karma of type {} from {}'.format(karma_type, member_id))
        else:
            await ctx.channel.send('Karma Type not recognized, only following are valid karma types {}'
                                   .format(self._configManager.karma_categories))
