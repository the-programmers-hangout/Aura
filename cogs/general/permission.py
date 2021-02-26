import logging

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import guild_only

from core.decorator import has_required_role
from util.config import config
from util.constants import aura_permissions, embed_color, bold_field
from util.embedutil import add_filler_fields
from util.permission import permission_map, write_permissions

log = logging.getLogger(__name__)


class PermissionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @guild_only()
    @has_required_role(command_name="getpermission")
    @commands.command(
        name="getpermission",
        brief="get the permission of the provided command",
        usage="{}getpermission (Command)".format(config["prefix"]),
    )
    async def get_permission(self, ctx, *, command_name: str):
        permission = permission_map[command_name]
        if permission is not None:
            await ctx.channel.send(f"{permission.upper()}")
        else:
            await ctx.channel.send(f"The command {command_name} does not exist.")

    @guild_only()
    @has_required_role(command_name="setpermission")
    @commands.command(
        name="setpermission",
        brief="set the permission of the provided command, help permission is unmodifiable",
        usage="{}setpermission [command] [permission]".format(config["prefix"]),
    )
    async def set_permission(self, ctx, command_name: str, permission: str):
        if command_name in permission_map.keys():
            if permission.lower() in aura_permissions:
                if command_name != "help":
                    permission_map[command_name] = permission.lower()
                    write_permissions()
                    await ctx.channel.send(
                        f"Permission for command: {command_name} has been changed to {permission}."
                    )
                else:
                    await ctx.channel.send("Permission of command is unmodifiable.")
            else:
                await ctx.channel.send(
                    f"Permission Level: {permission} is not valid.\n"
                    + f"Following are valid permission levels: {aura_permissions}."
                )
        else:
            await ctx.channel.send(f"The command {command_name} does not exist.")

    @guild_only()
    @has_required_role(command_name="showpermission")
    @commands.command(
        name="showpermission",
        brief="shows all commands with their currently set permissions.",
        usage="{}showpermission".format(config["prefix"]),
    )
    async def show_permission(self, ctx):
        embed: discord.Embed = Embed(
            color=embed_color,
            title="Permission Overview",
            description="shows all commands with their currently set permissions.",
        )
        embed.add_field(name=bold_field.format("help"), value="everyone")
        for key in permission_map.keys():
            embed.add_field(name=bold_field.format(key), value=permission_map[key])
        balanced_embed = add_filler_fields(embed, embed.fields)
        await ctx.channel.send(embed=balanced_embed)
