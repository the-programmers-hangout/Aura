import unittest
from unittest import mock

import mongomock
import pytest

from cogs.karma.producer import KarmaProducer
from core.model.member import KarmaMember
from core.service.karma_service import KarmaService, BlockerService
from tests.helpers import message_instance, guild_instance

if __name__ == '__main__':
    unittest.main()


# Verify that karma_services methods are working properly on a mocked mongodb
class KarmaChange(unittest.TestCase):
    karma_storage = mongomock.MongoClient().db.karma
    karma_service = KarmaService(karma_storage)
    karma_member = KarmaMember('1', '1', '1', '1')

    def test_karma_increases(self):
        self.karma_service.upsert_karma_member(self.karma_member, True)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) == 1
        self.karma_service.upsert_karma_member(self.karma_member, True)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) == 2
        for doc in self.karma_service.aggregate_member_by_channels(self.karma_member):
            assert doc['karma'] == 2

    def test_karma_resets(self):
        self.karma_service.delete_all_karma(self.karma_member.guild_id,
                                            self.karma_member.member_id)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) is None


# Verify that karma giving works on all possible permutations
class KarmaGiving(unittest.TestCase):
    karma_storage = mongomock.MongoClient().db.karma
    blacklisted = mongomock.MongoClient().db.blacklist
    blocker_service = BlockerService(blacklisted)
    karma_service = KarmaService(karma_storage)
    karma_producer = KarmaProducer(mock.MagicMock(), karma_service=karma_service, blocker_service=blocker_service)

    dummy_wrong_message_content = 'lmao <@1>'
    dummy_correct_message_content = 'thanks <@1>'

    pytestmark = pytest.mark.asyncio

    async def test_karma_given(self):
        message_instance.content = 'thanks <@1>'
        is_valid = await self.karma_producer.validate_message(message=message_instance, guild=guild_instance)
        assert is_valid
