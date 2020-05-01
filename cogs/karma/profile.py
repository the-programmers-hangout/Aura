from discord.ext import commands

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService
from util.config import ConfigStore


# Karma Profile Class, users other than moderators and admins can only see their own karma or profile.
# Moderators and Admin Role Users can get the karma by issuing the command with the user id.
class KarmaProfile(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")
        self._karma_service = KarmaService()
        self._configManager = ConfigStore()
        self._config = self._configManager.config
        self._roles = self._configManager.roles

    # get karma of yourself without any arguments, get karma of others if admin or moderator with user_id.
    @commands.command()
    async def karma(self, ctx):
        guild_id: str = self._config['guild']
        guild = self._bot.get_guild(int(guild_id))
        roles = ctx.message.author.roles
        if len(ctx.message.mentions) == 1 and (self._roles['admin'] in [role.name for role in roles]
                                               or self._roles['moderator'] in [role.name for role in roles]):
            message = ctx.message
            member = message.mentions[0]
            if not self._bot.get_user(self._bot.user.id).mentioned_in(message) and guild.get_member(
                    member.id).mentioned_in(message):
                karma_member = KarmaMember(guild_id, member.id, )
                karma = self._karma_service.aggregate_member_karma(karma_member)
                await ctx.channel.send('{} has earned a total of {} karma'
                                       .format(member.name + '#' + member.discriminator, karma))
        elif len(ctx.message.mentions) == 0:
            karma_member = KarmaMember(self._config['guild'], ctx.message.author.id)
            karma = self._karma_service.aggregate_member_karma(karma_member)
            await ctx.channel.send('{} has earned a total of {} karma'
                                   .format(ctx.message.author.name + '#' + ctx.author.discriminator, karma))
