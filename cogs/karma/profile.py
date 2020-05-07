from discord.ext import commands

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService


# Karma Profile Class, users other than moderators and admins can only see their own karma or profile.
# Moderators and Admin Role Users can get the karma by issuing the command with the user id.
class KarmaProfile(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._karma_service = KarmaService()

    # get karma of yourself without any arguments, get karma of others with mention
    @commands.command(brief='get karma of a user or yourself', description='prefix karma or prefix karma user_mention')
    async def karma(self, ctx):
        guild_id: str = str(ctx.message.guild.id)
        guild = self._bot.get_guild(int(guild_id))
        message = ctx.message
        member = message.mentions[0]
        if not self._bot.get_user(self._bot.user.id).mentioned_in(message) and guild.get_member(
                member.id).mentioned_in(message):
            karma_member = KarmaMember(guild_id, member.id)
            karma = self._karma_service.aggregate_member_karma(karma_member)
            if karma is None:
                await ctx.channel.send('{} has earned a total of {} karma'
                                       .format(member.name + '#' + member.discriminator, 0))
            else:
                await ctx.channel.send('{} has earned a total of {} karma'
                                       .format(member.name + '#' + member.discriminator, karma))
        elif len(ctx.message.mentions) == 0:
            karma_member = KarmaMember(guild_id, ctx.message.author.id)
            karma = self._karma_service.aggregate_member_karma(karma_member)
            await ctx.channel.send('{} has earned a total of {} karma'
                                   .format(ctx.message.author.name + '#' + ctx.author.discriminator, karma))