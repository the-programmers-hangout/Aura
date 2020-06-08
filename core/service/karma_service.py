import datetime
import logging

from core.model.member import KarmaMember, Member
# karma database service class, perform operations on the configured mongodb.
from util.config import profile, config

log = logging.getLogger(__name__)


class KarmaService:

    def __init__(self, ds_collection):
        self._karma = ds_collection
        self._increase_karma = {"$inc": {'karma': 1}}

    # update or insert karma member if not exist on first karma
    # check on inc if inc or dec query should be applied.
    def upsert_karma_member(self, member: KarmaMember):
        member_dict = vars(member)
        logging.info('channel_query: {}'.format(member_dict))
        # return update result
        return self._karma.update_one(filter=member_dict, update=self._increase_karma,
                                      upsert=True)

    def delete_karma_member(self, member: KarmaMember):
        # return delete result
        return self._karma.delete_one(filter=dict(guild_id=member.guild_id, member_id=member.member_id,
                                                  channel_id=member.channel_id, message_id=member.message_id))

    # remove all karma, regardless of channel and message.
    def delete_all_karma(self, member: KarmaMember):
        # return delete result of deletion
        return self._karma.delete_many(filter=dict(guild_id=member.guild_id, member_id=member.member_id))

    # aggregate overall karma of a member
    def aggregate_member_by_karma(self, member: KarmaMember):
        pipeline = [{"$unwind": "$karma"}, {"$match": dict(member_id=member.member_id, guild_id=member.guild_id)},
                    {"$group": {"_id": {"member_id": "$member_id"}, "karma": {"$sum": "$karma"}}}]
        doc_cursor = self._karma.aggregate(pipeline)
        for doc in doc_cursor:
            # return global karma of member
            return doc['karma']

    # aggregate member by the channels they got karma from
    def aggregate_member_by_channels(self, member: KarmaMember):
        pipeline = [{"$unwind": "$karma"}, {"$match": dict(member_id=member.member_id, guild_id=member.guild_id)},
                    {"$group": {"_id": {"member_id": "$member_id", "channel_id": "$channel_id"},
                                "karma": {"$sum": "$karma"}}},
                    {"$sort": {"karma": -1}}, {"$limit": int(profile()['channels'])}]
        doc_cursor = self._karma.aggregate(pipeline)
        # return cursor containing documents generated through the pipeline
        return doc_cursor

    def aggregate_top_karma_members(self, guild_id: str, channel_id: str = '', time_span: int = 0):
        if channel_id == '':
            if time_span == 0:
                pipeline = [{"$unwind": "$karma"}, {"$match": dict(guild_id=guild_id)},
                            {"$group": {"_id": {"member_id": "$member_id"},
                                        "karma": {"$sum": "$karma"}}},
                            {"$sort": {"karma": -1}}, {"$limit": int(config['leaderboard'])}]
                doc_cursor = self._karma.aggregate(pipeline)
                # return cursor containing documents generated through the pipeline
                return doc_cursor
            else:
                pipeline = [{"$unwind": "$karma"},
                            {"$match": {"guild_id": guild_id,
                                        "created_date":
                                            {"$gt": datetime.datetime.utcnow() -
                                                    datetime.timedelta(days=time_span)}}},
                            {"$group": {"_id": {"member_id": "$member_id"},
                                        "karma": {"$sum": "$karma"}}},
                            {"$sort": {"karma": -1}}, {"$limit": int(config['leaderboard'])}]
                doc_cursor = self._karma.aggregate(pipeline)
                # return cursor containing documents generated through the pipeline
                return doc_cursor
        else:
            if time_span == 0:
                pipeline = [{"$unwind": "$karma"}, {"$match": dict(guild_id=guild_id, channel_id=channel_id)},
                            {"$group": {"_id": {"member_id": "$member_id", "channel_id": "$channel_id"},
                                        "karma": {"$sum": "$karma"}}},
                            {"$sort": {"karma": -1}}, {"$limit": int(config['leaderboard'])}]
                doc_cursor = self._karma.aggregate(pipeline)
                # return cursor containing documents generated through the pipeline
                return doc_cursor
            else:
                pipeline = [{"$unwind": "$karma"},
                            {"$match": {"guild_id": guild_id,
                                        "channel_id": channel_id,
                                        "created_date":
                                            {"$gt": datetime.datetime.utcnow() -
                                                    datetime.timedelta(days=time_span)}}},
                            {"$group": {"_id": {"member_id": "$member_id", "channel_id": "$channel_id"},
                                        "karma": {"$sum": "$karma"}}},
                            {"$sort": {"karma": -1}}, {"$limit": int(config['leaderboard'])}]
                doc_cursor = self._karma.aggregate(pipeline)
                # return cursor containing documents generated through the pipeline
                return doc_cursor

    # filter message id
    def find_message(self, message_id: str):
        return self._karma.find_one(filter=dict(message_id=message_id))


class BlockerService:

    def __init__(self, ds_collection):
        self._blacklist = ds_collection

    def blacklist(self, member: Member):
        member_dict = vars(member)
        # returns an update result
        return self._blacklist.update_one(filter=member_dict, update={'$set': member_dict}, upsert=True)

    def whitelist(self, member: Member):
        # returns a delete result
        return self._blacklist.delete_one(filter=vars(member))

    def find_member(self, member: Member):
        # returns the member if it finds it
        return self._blacklist.find_one(filter=vars(member))

    def find_all_blacklisted(self, guild_id):
        # returns a cursor of all blacklisted members found in the guild
        return self._blacklist.find(filter=dict(guild_id=guild_id), projection=dict(member_id=True))
