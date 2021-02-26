import unittest
from unittest import mock

import mongomock

from cogs.karma.producer import KarmaProducer
from core.model.member import KarmaMember
from core.service.mongo_service import KarmaMemberService
from core.service.validation_service import contains_valid_thanks
from tests.async_decorator import async_test

if __name__ == "__main__":
    unittest.main()


# Verify that karma_services methods are working properly on a mocked mongodb
class KarmaChange(unittest.TestCase):
    karma_source = mongomock.MongoClient().db.karma
    karma_service = KarmaMemberService(karma_source)
    karma_member = KarmaMember("1", "1", "1", "1")

    def test_karma_increased(self):
        self.karma_service.upsert_karma_member(self.karma_member)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) == 1
        self.karma_service.upsert_karma_member(self.karma_member)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) == 2
        for doc in self.karma_service.aggregate_member_by_channels(self.karma_member):
            assert doc["karma"] == 2

    def test_karma_reset(self):
        self.karma_service.delete_all_karma(self.karma_member)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) is None


# Verify that karma messages are identified correctly
class KarmaDetection(unittest.TestCase):
    karma_producer = KarmaProducer(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())

    dummy_wrong_message_content = "laughing out loud brother"
    dummy_wrong_message_content_2 = '"thanks dude"'
    dummy_wrong_message_content_3 = "> thanks obama"
    dummy_correct_message_content = "thanks camel"
    dummy_correct_message_content_2 = "Thanks birdie"
    dummy_correct_message_content_3 = "ty it was 3 > 2"
    dummy_correct_message_content_4 = "thank You horse"

    @async_test
    async def test_messages_identified_correctly(self):
        assert not await contains_valid_thanks(self.dummy_wrong_message_content)
        assert not await contains_valid_thanks(self.dummy_wrong_message_content_2)
        assert not await contains_valid_thanks(self.dummy_wrong_message_content_3)
        assert await contains_valid_thanks(self.dummy_correct_message_content)
        assert await contains_valid_thanks(self.dummy_correct_message_content_2)
        assert await contains_valid_thanks(self.dummy_correct_message_content_3)
        assert await contains_valid_thanks(self.dummy_correct_message_content_4)
