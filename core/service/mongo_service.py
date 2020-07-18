import datetime
import logging

from pymongo.results import UpdateResult, DeleteResult

from core.model.member import KarmaMember, Member
from util.config import profile, config

log = logging.getLogger(__name__)


class KarmaMemberService:

    def __init__(self, ds_collection):
        # karma database service class, perform operations on the configured mongodb.
        self._karma = ds_collection
        self._increase_karma = {"$inc": {'karma': 1}}

    # update or insert karma member if not exist on first karma
    # check on inc if inc or dec query should be applied.
    def upsert_karma_member(self, member: KarmaMember) -> UpdateResult:
        """
        update a karma member, upsert is used in case there is no karma member to update yet.
        :param member: karma member created and to be inserted/updated in the connected mongodb.
        :return: update result
        """
        member_dict = vars(member)
        logging.info('channel_query: {}'.format(member_dict))
        # return update result
        return self._karma.update_one(filter=member_dict, update=self._increase_karma,
                                      upsert=True)

    def delete_single_karma(self, member: KarmaMember) -> DeleteResult:
        """
        delete a single karma member, so it removes a single karma of a member.
        :param member: karma member to remove
        :return: delete result
        """
        # return delete result
        return self._karma.delete_one(filter=dict(guild_id=member.guild_id, member_id=member.member_id,
                                                  channel_id=member.channel_id, message_id=member.message_id))

    def delete_all_karma(self, member: KarmaMember) -> DeleteResult:
        """
        remove all karma of a single member, regardless of channel.
        :param member: which karma is to be completely removed.
        :return: delete result
        """
        # return delete result of deletion
        return self._karma.delete_many(filter=dict(guild_id=member.guild_id, member_id=member.member_id))

    # aggregate overall karma of a member
    def aggregate_member_by_karma(self, member: KarmaMember):
        """
        aggregate karma in mongodb by member in a guild
        :param member: with whom to aggregate the collections
        :return: karma of member
        """
        pipeline = [{"$unwind": "$karma"}, {"$match": dict(member_id=member.member_id, guild_id=member.guild_id)},
                    {"$group": {"_id": {"member_id": "$member_id"}, "karma": {"$sum": "$karma"}}}]
        doc_cursor = self._karma.aggregate(pipeline)
        for doc in doc_cursor:
            # return global karma of member
            return doc['karma']

    def aggregate_member_by_channels(self, member: KarmaMember):
        """
        aggregate karma by channels in a guild from a single member
        :param member: the member whose karma to aggregate by channels.
        :return: database cursor which contains the results (channel id's and their karma)
        """
        pipeline = [{"$unwind": "$karma"}, {"$match": dict(member_id=member.member_id, guild_id=member.guild_id)},
                    {"$group": {"_id": {"member_id": "$member_id", "channel_id": "$channel_id"},
                                "karma": {"$sum": "$karma"}}},
                    {"$sort": {"karma": -1}}, {"$limit": int(profile()['channels'])}]
        doc_cursor = self._karma.aggregate(pipeline)
        # return cursor containing documents generated through the pipeline
        return doc_cursor

    def aggregate_top_karma_members(self, guild_id: str, channel_id: str = '', time_span: int = 0):
        """
        aggregate top karma members of a guild, optionally with a channel_id or time_span
        :param guild_id: guild to aggregate top members for
        :param channel_id: channel to filter out the results
        :param time_span: time span to filter out the results
        :return: database cursor containing member information and karma
        """
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

    def find_message(self, message_id: str):
        """
        find a message by its id.
        :param message_id: id of the message to find
        :return: karma member whose message id is equal to the parameter message id
        """
        return self._karma.find_one(filter=dict(message_id=message_id))


class KarmaChannelService:
    def __init__(self, ds_collection):
        self._karma = ds_collection

    def aggregate_top_karma_channels(self, guild_id: str, time_span: int = 0):
        # TODO has to be used in a cog
        if time_span == 0:
            pipeline = [{"$unwind": "$karma"}, {"$match": dict(guild_id=guild_id)},
                        {"$group": {"_id": {"channel_id": "$channel_id"},
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
                        {"$group": {"_id": {"channel_id": "$channel_id"},
                                    "karma": {"$sum": "$karma"}}},
                        {"$sort": {"karma": -1}}, {"$limit": int(config['leaderboard'])}]
            doc_cursor = self._karma.aggregate(pipeline)
            # return cursor containing documents generated through the pipeline
            return doc_cursor


class BlockerService:

    def __init__(self, ds_collection):
        self._blacklist = ds_collection

    def blacklist(self, member: Member) -> UpdateResult:
        """
        blacklist a member, no matter if it is already blacklisted or not.
        :param member: member to blacklist from giving out karma.
        :return: update result
        """
        member_dict = vars(member)
        # returns an update result
        return self._blacklist.update_one(filter=member_dict, update={'$set': member_dict}, upsert=True)

    def whitelist(self, member: Member) -> DeleteResult:
        """
        whitelist a member, no matter if it isn't blacklisted anymore or not.
        :param member: member to whitelist to allow them to give out karma once again.
        :return: delete result
        """
        # returns a delete result
        return self._blacklist.delete_one(filter=vars(member))

    def find_member(self, member: Member):
        """
        looks for a member inside the blacklist
        :param member: member to check if is inside the blacklist
        :return: the member if he exists or None
        """
        return self._blacklist.find_one(filter=vars(member))

    def find_all_blacklisted(self, guild_id):
        """
        returns a cursor of all blacklisted members found in the guild
        :param guild_id: id of the guild whose blacklist is to be retrieved
        :return: database cursor with members
        """
        return self._blacklist.find(filter=dict(guild_id=guild_id), projection=dict(member_id=True))
