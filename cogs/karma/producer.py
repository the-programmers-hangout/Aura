import logging
import re
from collections import defaultdict

import discord
from discord.ext import commands
from discord.ext.commands import guild_only

from core import datasource
from core.model.member import KarmaMember, Member
from core.service.karma_service import KarmaService, BlockerService
from core.timer import KarmaSingleActionTimer
from util.config import config, thanks_list

log = logging.getLogger(__name__)


# Class that gives positive karma and negative karma on message deletion (take back last action)
class KarmaProducer(commands.Cog):

    def __init__(self, bot, karma_service=KarmaService(datasource.karma),
                 blocker_service=BlockerService(datasource.blacklist)):
        self.bot = bot
        self.karma_service = karma_service
        self.blocker_service = blocker_service
        self._members_on_cooldown = defaultdict(lambda: defaultdict(list))

    # give karma if message has thanks and correct mentions
    @guild_only()
    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id: int = message.guild.id
        if not message.author.bot:
            if await self.validate_message(message):
                if self.blocker_service.find_member(Member(str(guild_id), message.author.id)) is None:
                    await self.give_karma(message, message.guild, True)
                else:
                    if str(config['blacklist']['message']).lower() == 'true':
                        log.info('Sending Blacklist dm to {} in guild {}'.format(message.author.id, guild_id))
                        await message.author.send('You have been blacklisted from giving out Karma, '
                                                  'if you believe this to be an error contact {}.'
                                                  .format(config['blacklist']['entity']))
                    if str(config['blacklist']['emote']).lower() == 'true':
                        await message.add_reaction('☠️')

    # remove karma on deleted message of said karma message
    @guild_only()
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.give_karma(message, message.guild, False)

    # remove karma on deleted reaction of said karma message
    @guild_only()
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user):
        if user.id == self.bot.user.id:
            log.info(reaction.emoji)
            if reaction.emoji == '👍':
                await self.give_karma(reaction.message, reaction.message.guild, False)

    @guild_only()
    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        for reaction in reactions:
            if reaction.emoji == '👍':
                log.info('here')
                if reaction.me:
                    await self.give_karma(message, message.guild, False)

    # check if message is a valid message for karma
    async def validate_message(self, message) -> bool:
        # check if message has any variation of thanks
        if self.has_thanks(message.content) and len(message.mentions) > 0:
            return True
        else:
            return False

    # check if message has thanks by using regex
    def has_thanks(self, message) -> bool:
        pattern = r'\b{}\b'
        for thanks in thanks_list():
            if re.search(re.compile(pattern.format(thanks), re.IGNORECASE), message) is not None:
                return True
        return False

    # give karma to all users in a message except author, other bots or aura itself.
    # logged to a configured channel with member name & discriminator, optionally with nickname
    # cooldown author after successfully giving karma
    async def give_karma(self, message: discord.Message, guild: discord.Guild, inc: bool):
        for mention in set(message.mentions):
            member = mention
            if member.id != message.author.id and member.id != self.bot.user.id and not \
                    self.bot.get_user(member.id).bot:
                if member.id not in self._members_on_cooldown[guild.id][message.author.id]:
                    karma_member = KarmaMember(guild.id, member.id, message.channel.id, message.id)
                    if inc:
                        self.karma_service.upsert_karma_member(karma_member)
                        await self.cooldown_user(guild.id, message.author.id, member.id)
                        await self.notify_member(message, member)
                    else:
                        karma_member.karma = 1
                        self.karma_service.delete_karma_member(karma_member)
                        log.info('{} gave karma to {} in guild {} with inc {}'
                             .format(message.author.id, member.id, guild.id, inc))
                else:
                    log.info('Sending configured cooldown response to {} in guild {}'
                             .format(message.author.id, guild.id))
                    if str(config['karma']['time-emote']).lower() == "true":
                        await message.add_reaction('🕒')
                    if str(config['karma']['time-message']).lower() == "true":
                        await self.bot.get_channel(message.channel.id) \
                            .send('Sorry {}, your karma for {} needs time to recharge'
                                  .format(message.author.mention, member.name))

    # notify user about successful karma gain
    async def notify_member(self, message, member):
        if str(config['karma']['log']).lower() == 'true':
            if member.nick is None:
                await self.bot.get_channel(int(config['channel']['log'])).send(
                    '{} earned karma in {}. {}'
                        .format(member.name + '#'
                                + member.discriminator,
                                message.channel.mention,
                                message.jump_url))
            else:
                await self.bot.get_channel(int(config['channel']['log'])).send(
                    '{} ({}) earned karma in {}. {}'.format(member.name + '#'
                                                            + member.discriminator,
                                                            member.nick,
                                                            message.channel.mention,
                                                            message.jump_url))
        if str(config['karma']['message']).lower() == 'true':
            await self.bot.get_channel(message.channel.id).send('Congratulations {}, you have earned karma.'
                                                                .format(member.mention))
        if str(config['karma']['emote']).lower() == 'true':
            await message.add_reaction('👍')

    # create new timer and add the user to it
    async def cooldown_user(self, guild_id: int, giver_id: int, receiver_id: int) -> None:
        self._members_on_cooldown[guild_id][giver_id].append(receiver_id)
        await KarmaSingleActionTimer(self.remove_from_cooldown, int(config['cooldown']),
                                     guild_id, giver_id, receiver_id).start()

    # remove user from cooldown after time runs out
    async def remove_from_cooldown(self, guild_id: int, giver_id: int, receiver_id: int) -> None:
        self._members_on_cooldown[guild_id][giver_id].remove(receiver_id)
