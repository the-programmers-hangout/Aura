from core.datasource import DataSource
from core.model.member import KarmaMember


# karma database service class, perform operations on the configured mongodb.
from util.config import config


class KarmaService:

    def __init__(self):
        self._karma = DataSource(config['database']['host'], config['database']['port'],
                                 config['database']['username'], config['database']['password'],
                                 config['database']['name']).db.karma
        self._filter_query = dict(guild_id="", member_id="")
        self._channel_query = dict(guild_id="", member_id="", channel_id="")
        self._increase_karma = {"$inc": {'karma': 1}}
        self._decrease_karma = {"$inc": {'karma': -1}}

    # update or insert karma member if not exist on first karma
    # check on inc if inc or dec query should be applied.
    def upsert_karma_member(self, member: KarmaMember, inc: bool) -> None:
        self._channel_query['guild_id'] = member.guild_id
        self._channel_query['member_id'] = member.member_id
        self._channel_query['channel_id'] = member.channel_id
        if inc:
            self._karma.update_one(filter=self._channel_query, update=self._increase_karma,
                                   upsert=True)
        else:
            self._karma.update_one(filter=self._channel_query, update=self._decrease_karma,
                                   upsert=False)

    # remove all karma, regardless of channel
    def delete_all_karma(self, guild_id: str, member_id: str) -> None:
        filter_member = dict(guild_id=guild_id, member_id=member_id)
        self._karma.delete_many(filter=filter_member)

    # aggregate karma of member for different channels
    def aggregate_member_karma(self, member: KarmaMember) -> int:
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        pipeline = [{"$unwind": "$karma"}, {"$match": self._filter_query},
                    {"$group": {"_id": {"member_id": "$member_id"}, "karma": {"$sum": "$karma"}}}]
        print(pipeline)
        document = self._karma.aggregate(pipeline)
        if document is None:
            return 0
        else:
            for doc in document:
                return doc['karma']


# class BlockerService:

