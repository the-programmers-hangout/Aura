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
from util.config import config, thanks_list, roles

log = logging.getLogger(__name__)

revoke_string = 'If you {}, didn\'t intend to give karma to this person, react to your thanks message with a 👎'


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
            # validate the message, is it a karma message?
            if await self.validate_message(message):
                # check if member is blacklisted
                if self.blocker_service.find_member(Member(str(guild_id), message.author.id)) is None:
                    # not blacklisted try to give karma
                    await self.give_karma(message, message.guild)
                else:
                    # is blacklisted, check configuration on how to tell the user he is blacklisted
                    if str(config['blacklist']['dm']).lower() == 'true':
                        log.info('Sending Blacklist dm to {} in guild {}'.format(message.author.id, guild_id))
                        await message.author.send('You have been blacklisted from giving out Karma, '
                                                  'if you believe this to be an error contact {}.'
                                                  .format(config['blacklist']['contact']))
                    if str(config['blacklist']['emote']).lower() == 'true':
                        await message.add_reaction('☠️')

    # remove karma on deleted message of said karma message
    @guild_only()
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # find message id in db
        if self.karma_service.find_message(str(message.id)) is not None:
            await self.remove_karma(message, message.guild, 'message delete')

    # remove karma on deleted reaction of said karma message
    @guild_only()
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user):
        # user args is the one who made the reaction according to docs
        if user.id == self.bot.user.id:
            # if aura made this reaction then it was very clearly a karma mesasge
            if reaction.emoji == '👍':
                message = reaction.message
                # find message id in db
                if self.karma_service.find_message(str(message.id)) is not None:
                    await self.remove_karma(message, message.guild, 'reaction remove')

    @guild_only()
    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        for reaction in reactions:
            if reaction.emoji == '👍':
                # reaction me is very much the same as checking the user id
                # was the reaction made by aura
                if reaction.me:
                    # find message id in db
                    if self.karma_service.find_message(str(message.id)) is not None:
                        await self.remove_karma(message, message.guild, 'reaction clear')

    @guild_only()
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if self.karma_service.find_message(str(reaction.message.id)) is not None:
            if reaction.emoji == '👎':
                if reaction.message.author.id == user.id:
                    await self.remove_karma(reaction.message, reaction.message.guild, 'self emoji clear')

    @guild_only()
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if str(config['edit']).lower() == 'true':
            before_valid = self.validate_message(before)
            after_valid = self.validate_message(after)
            if before_valid and after_valid:
                print()
            elif before_valid and not after_valid:
                # remove karma given out through karma message.
                await self.remove_karma(after, after.guild, 'message edit')
            elif after_valid and not before_valid:
                # all new karma to give out
                await self.give_karma(after, after.guild)

    # check if message is a valid message for karma
    async def validate_message(self, message) -> bool:
        # check if message has any variation of thanks + at least one user mention
        if self.contains_valid_thanks(message.content) and len(message.mentions) > 0:
            return True
        else:
            return False

    # check if message has thanks by using regex
    def contains_valid_thanks(self, message) -> bool:
        pattern = r'\b{}\b'
        invalid_pattern = r'\"{}\b{}\b{}\"'
        invalid_regex = '[0-9a-zA-z\s]*'  # message containing " and any character in between
        for thanks in thanks_list():
            thanks: str = thanks.strip()
            valid_match = re.search(re.compile(pattern.format(thanks), re.IGNORECASE), message)
            invalid_match = re.search(re.compile(invalid_pattern.format(invalid_regex, thanks, invalid_regex)), message)
            if valid_match is not None and invalid_match is None:
                return True
        return False

    # give karma to all users in a message except author, other bots or aura itself.
    # logged to a configured channel with member name & discriminator, optionally with nickname
    # cooldown giver-receiver combo after successfully giving karma
    async def give_karma(self, message: discord.Message, guild: discord.Guild):
        # walk through the mention list which contains discord: Members
        for mention in set(message.mentions):
            member = mention
            # filter out message author, aura and other bots
            if member.id != message.author.id and member.id != self.bot.user.id and not \
                    self.bot.get_user(member.id).bot:
                # check if giver-receiver combo on cooldown
                if member.id not in self._members_on_cooldown[guild.id][message.author.id]:
                    karma_member = KarmaMember(guild.id, member.id, message.channel.id, message.id)
                    self.karma_service.upsert_karma_member(karma_member)
                    await self.cooldown_user(guild.id, message.author.id, member.id)
                    await self.notify_member_gain(message, member)
                    log.info('{} gave karma to {} in guild {}'
                             .format(message.author.id, member.id, guild.id))
                else:
                    log.info('Sending configured cooldown response to {} in guild {}'
                             .format(message.author.id, guild.id))
                    if str(config['karma']['time-emote']).lower() == "true":
                        await message.add_reaction('🕒')
                    if str(config['karma']['time-message']).lower() == "true":
                        await self.bot.get_channel(message.channel.id) \
                            .send('Sorry {}, your karma for {} needs time to recharge'
                                  .format(message.author.mention, member.name))

    # remove karma with event
    async def remove_karma(self, message: discord.Message, guild: discord.Guild, reason: str):
        # walk through the mention list which contains discord: Members
        for mention in set(message.mentions):
            member = mention
            karma_member = KarmaMember(guild.id, member.id, message.channel.id, message.id)
            karma_member.karma = 1
            deletion_result = self.karma_service.delete_karma_member(karma_member)
            if deletion_result.deleted_count == 1:
                await self.notify_member_removal(message, member, reason)

    # notify user about successful karma gain
    async def notify_member_gain(self, message, member):
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
                                                            message.jump_url)
                    + revoke_string)
        if str(config['karma']['message']).lower() == 'true':
            await self.bot.get_channel(message.channel.id).send('Congratulations {}, you have earned karma from {}. '
                                                                .format(member.mention, message.author.mention)
                                                                + revoke_string.format(message.author.mention))
        if str(config['karma']['emote']).lower() == 'true':
            await message.add_reaction('👍')

    async def notify_member_removal(self, message, member, event_type):
        if config['karma']['log']:
            if event_type == 'message delete':
                await self.bot.get_channel(int(config['channel']['log'])).send(
                    'karma for {} was removed through event: {} :: in {}'.format(
                        member.name + '#' + member.discriminator,
                        event_type, message.channel.mention))
            else:
                await self.bot.get_channel(int(config['channel']['log'])).send(
                    'karma for {} was removed through event: {} :: in {} :: {}'.format(
                        member.name + '#' + member.discriminator,
                        event_type,
                        message.channel.mention,
                        message.jump_url))

    # create new timer and add the user to it
    async def cooldown_user(self, guild_id: int, giver_id: int, receiver_id: int) -> None:
        self._members_on_cooldown[guild_id][giver_id].append(receiver_id)
        await KarmaSingleActionTimer(self.remove_from_cooldown, int(config['cooldown']),
                                     guild_id, giver_id, receiver_id).start()

    # remove user from cooldown after time runs out
    async def remove_from_cooldown(self, guild_id: int, giver_id: int, receiver_id: int) -> None:
        self._members_on_cooldown[guild_id][giver_id].remove(receiver_id)
