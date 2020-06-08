import discord


def member_has_role(member: discord.Member, role: str):
    role = discord.utils.find(lambda r: r.name == role, member.roles)
    return role is not None

