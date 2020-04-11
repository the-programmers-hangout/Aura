from collections import defaultdict

from discord.ext import commands

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService
from core.timer import KarmaCooldownTimer
from util.config import ConfigManager


class KarmaProvider:

    def __init__(self, bot, karma_type):
        self._bot = bot
        self._karma_type = karma_type
        self._karma_service = KarmaService()
        self._config = ConfigManager().config
        self._members_on_cooldown = defaultdict(list)

    async def give_karma(self, ctx):
        # check if message has a mention
        if len(ctx.message.role_mentions) == 0:
            if len(ctx.message.mentions) != 1:
                await ctx.channel.send(str(self._config['default-messages']['no-mention'])
                                       .format(self._config['prefix'], self._karma_type))
            else:
                guild_id: int = int(self._config['guild'])
                guild = self._bot.get_guild(guild_id)
                message = ctx.message
                member = message.mentions[0]
                if self._bot.get_user(self._bot.user.id).mentioned_in(message):
                    await ctx.channel.send(str(self._config['default-messages']['bot'])
                                           .format(message.author.mention))
                elif guild.get_member(message.author.id).mentioned_in(message):
                    await ctx.channel.send(str(self._config['default-messages']['self'])
                                           .format(message.author.mention))
                elif self._bot.get_user(member.id).bot:
                    await ctx.channel.send(str(self._config['default-messages']['other-bot'])
                                           .format(message.author.mention))
                else:
                    if guild.get_member(member.id).mentioned_in(message):
                        if message.author.id not in self._members_on_cooldown[guild_id]:
                            karma_member = KarmaMember(guild_id, member.id, self._karma_type)
                            self._karma_service.upsert_karma_member(karma_member)
                            await self.cooldown_user(guild_id, message.author.id)
                            await ctx.channel.send(str(self._config['default-messages']['gain'])
                                                   .format(member.mention, self._karma_type))
                        else:
                            await ctx.channel.send(str(self._config['default-messages']['cooldown'])
                                                   .format(message.author.mention, self._karma_type))

        else:
            await ctx.channel.send(str(self._config['default-messages']['role-mention'])
                                   .format(ctx.message.author.mention))

    async def cooldown_user(self, guild_id: int, member_id: int):
        self._members_on_cooldown[guild_id].append(member_id)
        await KarmaCooldownTimer(self.remove_from_cooldown, int(self._config['cooldown']), guild_id, member_id).start()

    async def remove_from_cooldown(self, guild_id: int, member_id: int):
        await self._members_on_cooldown[guild_id].remove(member_id)


class Helpful(commands.Cog, KarmaProvider):

    def __init__(self, bot):
        super().__init__(bot, 'helpful')

    @commands.command()
    async def helpful(self, ctx):
        await self.give_karma(ctx)


class Informative(commands.Cog, KarmaProvider):

    def __init__(self, bot):
        super().__init__(bot, 'informative')

    @commands.command()
    async def informative(self, ctx):
        await self.give_karma(ctx)


class Kind(commands.Cog, KarmaProvider):

    def __init__(self, bot):
        super().__init__(bot, 'kind')

    @commands.command()
    async def kind(self, ctx):
        await self.give_karma(ctx)


class Creative(commands.Cog, KarmaProvider):

    def __init__(self, bot):
        super().__init__(bot, 'creative')

    @commands.command()
    async def creative(self, ctx):
        await self.give_karma(ctx)


class Funny(commands.Cog, KarmaProvider):

    def __init__(self, bot):
        super().__init__(bot, 'funny')

    @commands.command()
    async def funny(self, ctx):
        await self.give_karma(ctx)
