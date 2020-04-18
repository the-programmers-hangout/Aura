import pymongo

from core.database import Database
from core.model.member import KarmaMember
from util.config import ConfigStore


class KarmaService:

    def __init__(self):
        self._configManager = ConfigStore()
        self._config = self._configManager.config
        self._karma = Database(self._config['database']['host'], self._config['database']['port'],
                               self._config['database']['username'], self._config['database']['password'],
                               self._config['database']['name']).db.karma
        self._filter_query = dict(guild_id="", member_id="")
        self._channel_query = dict(guild_id="", member_id="", channel_id="{}")
        self._increase_karma = {"$inc": {'karma': int(1)}}

    def upsert_karma_member(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._filter_query['channel_id'] = member.channel_id
        self._karma.update_one(filter=self._filter_query, update=self._increase_karma,
                               upsert=True)

    def get_top_karma_members(self, guild_id: str, karma_type: str):
        filter_guild = dict(guild_id=guild_id, karma_type=karma_type)
        return self._karma.find(filter_guild).sort([('karma', pymongo.ASCENDING)])\
            .limit(self._config['leaderboard']['limit'])

    # resets all karma of member
    def delete_all_karma(self, guild_id: str, member_id: str):
        filter_member = dict(guild_id=guild_id, member_id=member_id)
        self._karma.delete_many(filter=filter_member)

    def get_karma_from_karma_member(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        document = self._karma.find_one(filter=self._filter_query)
        if document is None:
            return 0
        else:
            return document['karma']
