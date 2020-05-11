from core.datasource import DataSource
from core.model.member import KarmaMember, Member

# karma database service class, perform operations on the configured mongodb.
from util.config import config, profile


class KarmaService:

    def __init__(self, ds_collection):
        self._karma = ds_collection
        self._filter_query = dict(guild_id="", member_id="")
        self._channel_query = dict(guild_id="", member_id="", channel_id="", message_id="")
        self._increase_karma = {"$inc": {'karma': 1}}
        self._decrease_karma = {"$inc": {'karma': -1}}

    # update or insert karma member if not exist on first karma
    # check on inc if inc or dec query should be applied.
    def upsert_karma_member(self, member: KarmaMember, inc: bool):
        self._channel_query['guild_id'] = member.guild_id
        self._channel_query['member_id'] = member.member_id
        self._channel_query['channel_id'] = member.channel_id
        self._channel_query['message_id'] = member.message_id
        if inc:
            # return update result
            return self._karma.update_one(filter=self._channel_query, update=self._increase_karma,
                                          upsert=True)
        else:
            # return delete result
            return self._karma.delete_one(filter=self._channel_query)

    # remove all karma, regardless of channel and message.
    def delete_all_karma(self, guild_id: str, member_id: str):
        filter_member = dict(guild_id=guild_id, member_id=member_id)
        # return delete result of deletion
        return self._karma.delete_many(filter=filter_member)

    # aggregate overall karma of a member
    def aggregate_member_by_karma(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        pipeline = [{"$unwind": "$karma"}, {"$match": self._filter_query},
                    {"$group": {"_id": {"member_id": "$member_id"}, "karma": {"$sum": "$karma"}}}]
        doc_cursor = self._karma.aggregate(pipeline)
        for doc in doc_cursor:
            # return global karma of member
            return doc['karma']

    # aggregate member by the channels they got karma from
    def aggregate_member_by_channels(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        pipeline = [{"$unwind": "$karma"}, {"$match": self._filter_query},
                    {"$group": {"_id": {"member_id": "$member_id", "channel_id": "$channel_id"},
                                "karma": {"$sum": "$karma"}}}, {"$limit": profile()['channels']},
                    {"$sort": {"karma": -1}}]
        doc_cursor = self._karma.aggregate(pipeline)
        # return cursor containing documents generated through the pipeline
        return doc_cursor


class BlockerService:

    def __init__(self, ds_collection):
        self._blacklist = ds_collection
        self._filter_query = dict(guild_id="", member_id="")

    def blacklist(self, member: Member):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        # returns an update result
        return self._blacklist.update_one(filter=self._filter_query, update={'$set': {
            'guild_id': '{}'.format(member.guild_id),
            'member_id': '{}'.format(member.member_id)
        }}, upsert=True)

    def whitelist(self, member: Member):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        # returns a delete result
        return self._blacklist.delete_one(filter=self._filter_query)

    def find_member(self, member: Member):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        # returns the member if it finds it
        return self._blacklist.find_one(filter=self._filter_query)
