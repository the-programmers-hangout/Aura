import yaml
from discord.ext import commands

# Class to return karma of a single user or the top of the particular karma type
from core.model.karma_member import KarmaMember
from core.service.karma_service import KarmaService


class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._karma_service = KarmaService()
        with open("config.yaml", 'r') as stream:
            self._config = yaml.safe_load(stream)

    @commands.command()
    async def karma(self, ctx, karma_type, *, content):
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
                                           .format(member.name, karma, karma_type))

    @commands.command()
    async def leaderboard(self, ctx, karma_type):
        print()
