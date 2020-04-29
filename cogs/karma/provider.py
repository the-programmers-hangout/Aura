import re
from collections import defaultdict

import discord
from discord.ext import commands

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService
from core.timer import KarmaCooldownTimer
from util.config import ConfigStore


class KarmaProvider(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")
        self._karma_service = KarmaService()
        self._configManager = ConfigStore()
        self._config = self._configManager.config
        self._members_on_cooldown = defaultdict(list)
        self._thanksList = ["thanks", "ty", "thank you"]

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id: int = int(self._config['guild'])
        guild = self._bot.get_guild(guild_id)
        if self.validate_message(message, guild):
            if message.author.id not in self._members_on_cooldown[guild.id]:
                await self.give_karma(message, guild, message.mentions[0], True)
            else:
                await message.channel.send("Sorry, {}. Your Karma needs some time to recharge."
                                           .format(message.author.mention))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild_id: int = int(self._config['guild'])
        guild = self._bot.get_guild(guild_id)
        await self.give_karma(message, guild, message.author.id, False)

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

    def has_thanks(self, message) -> bool:
        pattern = r'\b{}\b'
        for thanks in self._thanksList:
            if re.search(re.compile(pattern.format(thanks), re.IGNORECASE), message.content) is not None:
                return True
        return False

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
                    if self._bot.get_user(member.id).bot:
                        # other bot
                        return -1
                    else:
                        return 1
            else:
                return -1
        else:
            return -1

    async def give_karma(self, message: discord.Message, guild: discord.Guild, member: discord.Member, inc: bool):
        if guild.get_member(member.id).mentioned_in(message):
            karma_member = KarmaMember(guild.id, member.id, message.channel.id)
            self._karma_service.upsert_karma_member(karma_member)
            await self.cooldown_user(guild.id, message.author.id)

    async def cooldown_user(self, guild_id: int, member_id: int) -> None:
        self._members_on_cooldown[guild_id].append(member_id)
        await KarmaCooldownTimer(self.remove_from_cooldown, int(self._config['cooldown']), guild_id, member_id).start()

    async def remove_from_cooldown(self, guild_id: int, member_id: int) -> None:
        self._members_on_cooldown[guild_id].remove(member_id)
