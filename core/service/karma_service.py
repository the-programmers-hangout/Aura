from core.database import Database
from core.model.karma_member import KarmaMember


class KarmaService:

    def __init__(self):
        self._db = Database('mongo', 27017, 'aura').db
        self._filter_query = dict(guild_id="", member_id="", karma_type="")
        self._increase_karma = {"$inc": {'karma': int(1)}}

    def upsert_karma_member(self, member: KarmaMember):
        karma = self._db.karma
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._filter_query['karma_type'] = member.karma_type
        karma.update_one(filter=self._filter_query, update=self._increase_karma,
                         upsert=True)

    def get_top_karma_members(self, guild_id: int, limit: int):
        filter_guild = dict(guild_id=guild_id)
        return self._db.karma.find(filter=filter_guild).sort({'karma': 1}).limit(limit)

    def delete_karma_member(self, member: KarmaMember):
        print()

    def set_karma(self, member: KarmaMember):
        print()

    def get_karma_from_karma_member(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._filter_query['karma_type'] = member.karma_type
        document = self._db.karma.find_one(filter=self._filter_query)
        if document is None:
            return 0
        else:
            return document['karma']

    def cooldown_karma_giving_ability(self, member: KarmaMember):
        print()
