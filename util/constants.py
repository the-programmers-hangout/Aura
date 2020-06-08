from collections import defaultdict

from discord import Color

from util.config import karma_delete_emoji

zero_width_space = '\u200b'
revoke_message = 'If you {}, didn\'t intend to give karma to this person,' + \
                 ' react to the' + karma_delete_emoji + 'of your original thanks message'
leaderboard_usage = '{}leaderboard\n{}leaderboard <#channel_mention>' \
                    '\n{}leaderboard (global) (days) \n'\
                    '{}leaderboard ' \
                    '<#channel_mention> (days)'
embed_max_columns = 3  # 3 because discord embeds can have three fields in a line
embed_color = Color.dark_gold()
bold_field = "**{}**"
cog_mapping = defaultdict(list)
