from collections import defaultdict

from discord import Color

from util.config import karma_delete_emoji

zero_width_space: str = '\u200b'
revoke_message = 'If you {}, didn\'t intend to give karma to this person,' + \
                 ' react to the' + karma_delete_emoji + 'of your original thanks message'
leaderboard_usage = '{}leaderboard\n{}leaderboard <#channel_mention>' \
                    '\n{}leaderboard (global) (days) \n' \
                    '{}leaderboard ' \
                    '<#channel_mention> (days)'
embed_max_columns = 3  # 3 because discord embeds can have three fields in a line
embed_color = Color.dark_gold()
bold_field = "**{}**"
cog_map = defaultdict()  # cog name to cog class
aura_permissions = ['everyone', 'moderator', 'admin', 'owner']
hidden_config = ['token', 'owner', 'prefix', 'database', 'logging']


# version dict
def version():
    return dict(aura_version='1.17.1', python_version='3.8.2', discord_version='1.3.4')


# return the discord tag of the author of this bot
def author_discord():
    return 'arkencl#5579'


# return the link to the repository
def repository():
    return '[[Github]](https://github.com/arkencl/aura)'
