import logging
import re

import discord

log = logging.getLogger(__name__)

mention_pattern = r'[^@!<>]+'
mention_regex = re.compile(mention_pattern)


# convert member_list with mixed ids and members to a pure list of members
# the list returned only contains non-bot members
async def convert_content_to_member_set(ctx, argument_list):
    guild = ctx.guild
    pure_list = []
    logging.info('Conversion to pure list \n original list: {}'.format(argument_list))
    for content in argument_list:
        result = re.search(mention_regex, content)
        if result is not None:
            content = result.group(0)
        member = guild.get_member(int(content))
        if member is not None and not member.bot:
            pure_list.append(member)
    return set(pure_list)
