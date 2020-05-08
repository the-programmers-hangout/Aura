import re
from collections import defaultdict

import discord
from discord.ext import commands

from core.model.member import KarmaMember, Member
from core.service.karma_service import KarmaService, BlockerService
from core.timer import KarmaCooldownTimer

from util.config import config, thanks_list


# Class that gives positive karma and negative karma on message deletion (take back last action)
class KarmaProducer(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._karma_service = KarmaService()
        self._blocker_service = BlockerService()
        self.members_on_cooldown = defaultdict(list)

    # give karma if message has thanks and correct mentions
    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id: int = message.guild.id
        guild = self._bot.get_guild(guild_id)
        if self._blocker_service.find_member(Member(str(guild_id), message.author.id)) is None:
            if await self.validate_message(message, guild):
                if message.author.id not in self.members_on_cooldown[guild.id]:
                    await self.give_karma(message, guild, message.mentions[0], True)

    # remove karma on deleted message of said karma message
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild_id: int = message.guild.id
        guild = self._bot.get_guild(guild_id)
        if await self.validate_message(message, guild):
            await self.give_karma(message, guild, message.mentions[0], False)

    # check if message is a valid message for karma
    async def validate_message(self, message, guild) -> bool:
        # check if message has any variation of thanks
        if self.has_thanks(message):
            # filter out messages without incorrect mention
            mention_type: int = self.filter_mentions(message, guild)
            # give karma to user
            if mention_type > -1:
                if mention_type == 1:
                    return True
                else:
                    # use member name
                    print('not implemented yet')
        return False

    # check if message has thanks by using regex
    def has_thanks(self, message) -> bool:
        pattern = r'\b{}\b'
        for thanks in thanks_list():
            if re.search(re.compile(pattern.format(thanks), re.IGNORECASE), message.content) is not None:
                return True
        return False

    # returns -1 if mentions are incorrect for karma -> everything but user mention, mention of bot id
    # mention of author id himself, mention of karma bot id
    # return 0 if message has no mention
    # -> (will be handled in a future version where messages with no mentions are potentially considered).
    # return 1 if correct user mention
    def filter_mentions(self, message, guild) -> int:
        if len(message.role_mentions) == 0:
            if not self._bot.get_user(self._bot.user.id).mentioned_in(message) \
                    and not guild.get_member(message.author.id).mentioned_in(message):
                if len(message.mentions) > 1:
                    return -1
                elif len(message.mentions) == 0:
                    return 0
                else:
                    member = message.mentions[0]
                    if self._bot.get_user(member.id).bot \
                            or self._blocker_service.find_member(Member(guild.id, member.id)):
                        # other bot or blacklisted
                        return -1
                    else:
                        return 1
            else:
                return -1
        else:
            return -1

    # give karma to user.
    # logged to a configured channel with member name & discriminator, optionally with nickname
    # cooldown author after successfully giving karma
    async def give_karma(self, message: discord.Message, guild: discord.Guild, member: discord.Member, inc: bool):
        if guild.get_member(member.id).mentioned_in(message):
            karma_member = KarmaMember(guild.id, member.id, message.channel.id, message.id)
            self._karma_service.upsert_karma_member(karma_member, inc)
            if inc:
                if member.nick is None:
                    await self._bot.get_channel(int(config['channel']['log'])).send(
                        '{} earned karma in {}'
                            .format(member.name + '#'
                                    + member.discriminator,
                                    message.channel.mention))
                else:
                    await self._bot.get_channel(int(config['channel']['log'])).send(
                        '{} ({}) earned karma in {}'
                            .format(member.name + '#'
                                    + member.discriminator,
                                    member.nick,
                                    message.channel.mention))
            await self.cooldown_user(guild.id, message.author.id)

    # create new timer and add the user to it
    async def cooldown_user(self, guild_id: int, member_id: int) -> None:
        self.members_on_cooldown[guild_id].append(member_id)
        await KarmaCooldownTimer(self.remove_from_cooldown, int(config['cooldown']),
                                 guild_id, member_id).start()

    # remove user from cooldown after time runs out
    async def remove_from_cooldown(self, guild_id: int, member_id: int) -> None:
        self.members_on_cooldown[guild_id].remove(member_id)
