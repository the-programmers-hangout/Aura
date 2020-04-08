class KarmaMember:
    def __init__(self, guild_id, member_id, karma_type, karma):
        self._member = {"guild_id:" "{}".format(guild_id),
                        "member_id:" "{}".format(member_id),
                        "karma_type:" "{}".format(karma_type),
                        "karma:" "{}".format(karma)}
        self._guild_id = self._member['guild_id']
        self._member_id = self._member['member_id']
        self._karma_type = self._member['karma_tyüe']
        self._karma = self._member['karma']

    @property
    def guild_id(self):
        return self._guild_id

    @property
    def member_id(self):
        return self._member_id

    @property
    def karma_type(self):
        return self._karma_type

    @property
    def karma(self):
        return self._karma

    @property
    def document(self):
        return self._member
