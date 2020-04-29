from discord.ext import commands

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService
from util.config import ConfigStore


class KarmaProfile(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")
        self._karma_service = KarmaService()
        self._configManager = ConfigStore()
        self._config = self._configManager.config

    @commands.command()
    async def karma(self, ctx):
        karma_member = KarmaMember(self._config['guild'], ctx.message.author.id)
        karma = self._karma_service.aggregate_member_karma(karma_member)
        await ctx.channel.send('{} has earned a total of {} karma'
                               .format(ctx.message.author.name + '#' + ctx.author.discriminator, karma))
