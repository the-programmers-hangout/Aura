import datetime


class KarmaMember:
    # simple entity class for karma associated with a member
    def __init__(self, guild_id: str, member_id: str, channel_id: str = "", message_id: str = "", karma: int = 0):
        self.guild_id = str(guild_id)
        self.member_id = str(member_id)
        self.channel_id = str(channel_id)
        self.message_id = str(message_id)
        self.created_date = datetime.datetime.utcnow()
        self.karma = karma


# simple entity class for members for blacklisting purposes
class Member:
    def __init__(self, guild_id: str, member_id: str):
        self.guild_id = str(guild_id)
        self.member_id = str(member_id)
