import discord


def member_has_role(member: discord.Member, role_name: str) -> bool:
    """
    utility method to check if role exists within the members roles
    :param member: discord.Member to check for the role
    :param role_name: the name of the role
    :return: True if role exists in member.roles, False if not.
    """
    role_name = discord.utils.find(lambda r: r.name == role_name, member.roles)
    return role_name is not None

