import logging
import re
from typing import List, Set

import discord

log = logging.getLogger(__name__)

mention_pattern = r"[^@!<>]+"
mention_regex = re.compile(mention_pattern)


# convert member_list with mixed ids and members to a pure list of members
# the list returned only contains non-bot members
async def convert_content_to_member_set(
    ctx, argument_list: List[str]
) -> Set[discord.Member]:
    """
    convert member_list with mixed ids and members to a pure list of members
    the list returned only contains non-bot members
    :param ctx: context of the invocation
    :param argument_list: ids or mentions
    :return:
    """
    guild = ctx.guild
    pure_list = []
    logging.info("Conversion to pure list \n original list: {}".format(argument_list))
    for content in argument_list:
        result = re.search(mention_regex, content)
        if result is not None:
            content = result.group(0)
        member = guild.get_member(int(content))
        if member is not None and not member.bot:
            pure_list.append(member)
    return set(pure_list)


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
