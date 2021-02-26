import logging

import discord

from util.config import reaction_emoji

log = logging.getLogger(__name__)


def member_has_role(member: discord.Member, role_name: str) -> bool:
    """
    utility method to check if role exists within the members roles
    :param member: discord.Member to check for the role
    :param role_name: the name of the role
    :return: True if role exists in member.roles, False if not.
    """
    role_name = discord.utils.find(lambda r: r.name == role_name, member.roles)
    return role_name is not None


async def clear_reaction(reaction: discord.Reaction) -> None:
    """
    clears a reaction from a message if that reaction has an emoji from aura.
    :param reaction: reaction to clear
    :return: none
    """
    for aura_emoji in reaction_emoji().keys():
        if reaction.emoji == reaction_emoji()[aura_emoji]:
            await reaction.clear()
            return
