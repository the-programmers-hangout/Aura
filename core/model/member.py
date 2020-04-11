class KarmaMember:
    def __init__(self, guild_id, member_id, karma_type):
        self.member = dict(guild_id="{}".format(guild_id), member_id="{}".format(member_id),
                           karma_type="{}".format(karma_type), karma="")

    @property
    def guild_id(self):
        return self.member['guild_id']

    @property
    def member_id(self):
        return self.member['member_id']

    @property
    def karma_type(self):
        return self.member['karma_type']

    @property
    def karma(self):
        return self.member['karma']

    @property
    def document(self):
        return self.member
