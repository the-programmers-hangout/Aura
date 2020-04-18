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

    @commands.Cog.listener()
    async def on_message(self, ctx):
        guild_id: int = int(self._config['guild'])
        guild = self._bot.get_guild(guild_id)
        message = ctx.message
        if message.author.id not in self._members_on_cooldown[guild.id]:
            self.validate_message(message, guild)

    def validate_message(self, message, guild):
        # check if message has any variaton of thanks

        # filter out messages without incorrect mention
        mention_type: int = self.filter_mentions(message, guild)
        # give karma to user
        if mention_type > -1:
            if mention_type == 1:
                self.give_karma(message, guild, message.mentions[0])
            else:
                # use member name
                print('not implemented yet')

    def has_thanks(self, message) -> bool:
        print()

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

    def give_karma(self, message: discord.Message, guild: discord.Guild, member: discord.Member):
        if guild.get_member(member.id).mentioned_in(message):
            karma_member = KarmaMember(guild.id, member.id, message.channel.id)
            self._karma_service.upsert_karma_member(karma_member)
            await self.cooldown_user(guild.id, message.author.id)

    async def cooldown_user(self, guild_id: int, member_id: int) -> None:
        self._members_on_cooldown[guild_id].append(member_id)
        await KarmaCooldownTimer(self.remove_from_cooldown, int(self._config['cooldown']), guild_id, member_id).start()

    async def remove_from_cooldown(self, guild_id: int, member_id: int) -> None:
        await self._members_on_cooldown[guild_id].remove(member_id)
