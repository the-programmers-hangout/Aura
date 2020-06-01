import discord

from util.constants import zero_width_space, embed_max_columns


# embed to add filler fields, collection which to check, mode -> + or -
# counter (any other counter to apply) is default 0
def add_filler_fields(embed: discord.Embed, collection, mode: str = '+', counter: int = 0) -> discord.Embed:
    if mode == "+":
        if (len(collection) + counter) % embed_max_columns != 0:
            embed.add_field(name=zero_width_space, value=zero_width_space)
            if (len(collection) + counter + 1) % embed_max_columns != 0:
                embed.add_field(name=zero_width_space, value=zero_width_space)
    else:
        if (len(collection) - counter) % embed_max_columns != 0:
            embed.add_field(name=zero_width_space, value=zero_width_space)
        if (len(collection) - counter + 1) % embed_max_columns != 0:
            embed.add_field(name=zero_width_space, value=zero_width_space)
    return embed
