import re

import discord

from util.config import thanks_list


async def validate_message(message: discord.Message) -> bool:
    """
    Validates the message
    :param message: discord Message to validate for Aura
    :return: True if message is valid, False if not.
    """
    if await contains_valid_thanks(message.content):
        if len(message.mentions) > 0:
            return True
    else:
        return False


async def contains_valid_thanks(message: str) -> bool:
    """
    check if the message has a valid thanks keyword as configured. This is achieved
    by using several patterns and applying them to the message content of a discord Message
    :param message: message.content of a discord.Message
    :return: True if message has a valid keyword pattern, False if not.
    """
    pattern = r'\b{}\b'
    quotes_pattern = r'\"{}\b{}\b{}\"'
    greentext_pattern = r'^> {}\b{}\b{}$'
    any_char = r'[0-9a-zA-z\s]*'  # message containing " and any character in between
    for thanks in thanks_list():
        thanks: str = thanks.strip()
        valid_match = re.search(re.compile(pattern.format(thanks), re.IGNORECASE), message)
        invalid_quotes = re.search(re.compile(quotes_pattern.format(any_char, thanks, any_char)), message)
        invalid_greentext = re.search(re.compile(greentext_pattern.format(any_char, thanks, any_char),
                                                 flags=re.MULTILINE), message)
        if valid_match is not None and invalid_quotes is None and invalid_greentext is None:
            return True
    return False
