# simple entity class for karma associated with a member
class KarmaMember:
    def __init__(self, guild_id: str, member_id: str, channel_id: str = "", message_id: str = "", karma: int = ""):
        self.member = dict(guild_id="{}".format(guild_id), member_id="{}".format(member_id),
                           channel_id="{}".format(channel_id), message_id="{}".format(message_id), karma="")

    @property
    def guild_id(self):
        return self.member['guild_id']

    @property
    def member_id(self):
        return self.member['member_id']

    @property
    def channel_id(self):
        return self.member['channel_id']

    @property
    def message_id(self):
        return self.member['message_id']

    @property
    def karma(self):
        return self.member['karma']

    @property
    def document(self):
        return self.member


# simple entity class for members for blacklisting purposes
class Member:
    def __init__(self, guild_id: str, member_id: str):
        self.member = dict(guild_id="{}".format(guild_id), member_id="{}".format(member_id))

    @property
    def guild_id(self):
        return self.member['guild_id']

    @property
    def member_id(self):
        return self.member['member_id']
