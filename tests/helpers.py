from unittest import mock

import discord

# credits to the python servers discord bot source
# at https://github.com/python-discord/bot/blob/master/tests/helpers.py
from discord.ext.commands import Context

guild_data = {
    'id': 1,
    'name': 'guild',
    'region': 'Europe',
    'verification_level': 2,
    'default_notications': 1,
    'description': 'mocking is fun',
    'max_presences': 10_000,
    'max_members': 100_000,
    'preferred_locale': 'UTC',
    'owner_id': 1,
}
guild_instance = discord.Guild(data=guild_data, state=mock.MagicMock())

user_data = {
    'id': 1,
    'username': 'Walter',
    'avatar': None,
    'discriminator': '1234',
    'bot': False
}
user_instance = discord.User(data=user_data, state=mock.MagicMock)

channel_data = {
    'id': 1,
    'type': 'TextChannel',
    'name': 'channel',
    'parent_id': 1234567890,
    'topic': 'topic',
    'position': 1,
    'nsfw': False,
    'last_message_id': 1,
}
channel_instance = discord.TextChannel(data=channel_data, guild=guild_instance, state=mock.MagicMock)

message_data = {
    'id': 1,
    'webhook_id': 431341013479718912,
    'attachments': [],
    'embeds': [],
    'mentions': [],
    'application': 'Python Discord',
    'activity': 'mocking',
    'channel': channel_instance,
    'edited_timestamp': '2019-10-14T15:33:48+00:00',
    'type': 'message',
    'pinned': False,
    'mention_everyone': False,
    'tts': None,
    'content': 'content',
    'nonce': None,
}

message_instance = discord.Message(state=mock.MagicMock, channel=channel_instance, data=message_data)

context_instance = Context(message=message_instance, prefix=mock.MagicMock())

