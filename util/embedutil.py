import discord

from util.constants import zero_width_space, embed_max_columns


def add_filler_fields(embed: discord.Embed, collection, mode: str = "+", counter: int = 0) -> discord.Embed:
    """
    add filler fields (fields with zero width strings) to embeds so they look balanced.
    :param embed: the embed which needs filler fields applied to it.
    :param collection: the collection which is used to determine how many filler fields the embed needs
    either a collection of the fields in the embeds or something similar.
    :param mode: mode applies to the counter, can be + or -.
    :param counter: a counter variable may be used if the collection length is not sufficient.
    :return: embed with filler fields applied to it.
    """
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
