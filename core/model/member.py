class KarmaMember:
    def __init__(self, guild_id, member_id, channel_id=""):
        self.member = dict(guild_id="{}".format(guild_id), member_id="{}".format(member_id),
                           channel_id="{}".format(channel_id), karma="")

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
    def karma(self):
        return self.member['karma']

    @property
    def document(self):
        return self.member
