from discord.ext import commands

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService
from util.config import ConfigManager


class KarmaChecker(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")
        self._configManager = ConfigManager()
        self._config = self._configManager.config
        self._karma_service = KarmaService()

    @commands.command()
    async def karma(self, ctx, karma_type):
        if karma_type in self._configManager.karma_categories:
            if len(ctx.message.mentions) == 1:
                guild_id: int = int(self._config['guild'])
                guild = self._bot.get_guild(guild_id)
                message = ctx.message
                member = message.mentions[0]
                if not self._bot.get_user(self._bot.user.id).mentioned_in(message):
                    if guild.get_member(member.id).mentioned_in(message):
                        karma_member = KarmaMember(guild_id, member.id, karma_type)
                        karma = self._karma_service.get_karma_from_karma_member(karma_member)
                        await ctx.channel.send('{} has earned a total of {} {} karma'
                                               .format(member.name+'#'+member.discriminator, karma, karma_type))
            elif len(ctx.message.mentions) == 0:
                guild_id: int = int(self._config['guild'])
                karma_member = KarmaMember(guild_id, ctx.message.author.id, karma_type)
                karma = self._karma_service.get_karma_from_karma_member(karma_member)
                await ctx.channel.send('You have earned a total of {} {} karma'
                                       .format(karma, karma_type))
        else:
            await ctx.channel.send('Karma Type not recognized, only following are valid karma types {}'
                                   .format(self._configManager.karma_categories))
