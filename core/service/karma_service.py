from core.datasource import DataSource
from core.model.member import KarmaMember, Member

# karma database service class, perform operations on the configured mongodb.
from util.config import config, profile


class KarmaService:

    def __init__(self):
        self._karma = DataSource(config['database']['host'], config['database']['port'],
                                 config['database']['username'], config['database']['password'],
                                 config['database']['name']).db.karma
        self._filter_query = dict(guild_id="", member_id="")
        self._channel_query = dict(guild_id="", member_id="", channel_id="", message_id="")
        self._increase_karma = {"$inc": {'karma': 1}}
        self._decrease_karma = {"$inc": {'karma': -1}}

    # update or insert karma member if not exist on first karma
    # check on inc if inc or dec query should be applied.
    def upsert_karma_member(self, member: KarmaMember, inc: bool) -> None:
        self._channel_query['guild_id'] = member.guild_id
        self._channel_query['member_id'] = member.member_id
        self._channel_query['channel_id'] = member.channel_id
        self._channel_query['message_id'] = member.message_id

        if inc:
            self._karma.update_one(filter=self._channel_query, update=self._increase_karma,
                                   upsert=True)
        else:
            self._karma.delete_one(filter=self._channel_query)

    # remove all karma, regardless of channel
    def delete_all_karma(self, guild_id: str, member_id: str) -> None:
        filter_member = dict(guild_id=guild_id, member_id=member_id)
        self._karma.delete_many(filter=filter_member)

    # aggregate overall karma of a member
    def aggregate_member_by_karma(self, member: KarmaMember) -> int:
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        pipeline = [{"$unwind": "$karma"}, {"$match": self._filter_query},
                    {"$group": {"_id": {"member_id": "$member_id"}, "karma": {"$sum": "$karma"}}}]
        doc_cursor = self._karma.aggregate(pipeline)
        if doc_cursor is None:
            return 0
        else:
            for doc in doc_cursor:
                return doc['karma']

    def aggregate_member_by_channels(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        pipeline = [{"$unwind": "$karma"}, {"$match": self._filter_query},
                    {"$group": {"_id": {"member_id": "$member_id", "channel_id": "$channel_id"},
                                "karma": {"$sum": "$karma"}}}, {"$limit": profile()['channels']}]
        doc_cursor = self._karma.aggregate(pipeline)
        if doc_cursor is None:
            return None
        else:
            return doc_cursor


class BlockerService:

    def __init__(self):
        self._blacklist = DataSource(config['database']['host'], config['database']['port'],
                                     config['database']['username'], config['database']['password'],
                                     config['database']['name']).db.blacklist
        self._filter_query = dict(guild_id="", member_id="")

    def blacklist(self, member: Member):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._blacklist.update_one(filter=self._filter_query, update={'$set': {
            'guild_id': '{}'.format(member.guild_id),
            'member_id': '{}'.format(member.member_id)
        }}, upsert=True)

    def whitelist(self, member: Member):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._blacklist.delete_one(filter=self._filter_query)

    def find_member(self, member: Member):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        return self._blacklist.find_one(filter=self._filter_query)
