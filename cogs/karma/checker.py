from discord.ext import commands
from discord.ext.commands import has_any_role

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService
from util.config import ConfigStore


class KarmaChecker(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")
        self._configManager = ConfigStore()
        self._config = self._configManager.config
        self._karma_service = KarmaService()

    @has_any_role(ConfigStore().roles['admin'], ConfigStore().roles['moderator'])
    @commands.command()
    async def karma(self, ctx, karma_type):
        guild_id: str = self._config['guild']
        guild = self._bot.get_guild(int(guild_id))
        if karma_type in self._configManager.karma_categories:
            if len(ctx.message.mentions) == 1:
                message = ctx.message
                member = message.mentions[0]
                if not self._bot.get_user(self._bot.user.id).mentioned_in(message):
                    if guild.get_member(member.id).mentioned_in(message):
                        karma_member = KarmaMember(guild_id, member.id, karma_type)
                        karma = self._karma_service.get_karma_from_karma_member(karma_member)
                        await ctx.channel.send('{} has earned a total of {} {} karma'
                                               .format(member.name+'#'+member.discriminator, karma, karma_type))
        else:
            await ctx.channel.send('Karma Type not recognized, only following are valid karma types {}'
                                   .format(self._configManager.karma_categories))
