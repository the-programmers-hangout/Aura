from discord import Color

from util.config import karma_delete_emoji

zero_width_space = '\u200b'
revoke_message = 'If you {}, didn\'t intend to give karma to this person,' + \
                 ' react to the' + karma_delete_emoji + 'of your original thanks message'
embed_max_columns = 3  # 3 because discord embeds can have three fields in a line
embed_color = Color.dark_gold()
bold_field = "**{}**"
