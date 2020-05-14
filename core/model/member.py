# simple entity class for karma associated with a member
class KarmaMember:
    def __init__(self, guild_id: str, member_id: str, channel_id: str = "", message_id: str = "", karma: int = ""):
        self.guild_id = guild_id
        self.member_id = member_id
        self.channel_id = channel_id
        self.message_id = message_id
        self.karma = karma


# simple entity class for members for blacklisting purposes
class Member:
    def __init__(self, guild_id: str, member_id: str):
        self.guild_id = guild_id
        self.member_id = member_id