import unittest
from unittest import mock

from cogs.karma.producer import KarmaProducer

from core.model.member import KarmaMember
from core.service.karma_service import KarmaMemberService

import mongomock

if __name__ == "__main__":
    unittest.main()


# Verify that karma_services methods are working properly on a mocked mongodb
class KarmaChange(unittest.TestCase):
    karma_storage = mongomock.MongoClient().db.karma
    karma_service = KarmaMemberService(karma_storage)
    karma_member = KarmaMember("1", "1", "1", "1")

    def test_karma_increases(self) -> None:
        self.karma_service.upsert_karma_member(self.karma_member)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) == 1
        self.karma_service.upsert_karma_member(self.karma_member)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) == 2
        for doc in self.karma_service.aggregate_member_by_channels(self.karma_member):
            assert doc["karma"] == 2

    def test_karma_resets(self) -> None:
        self.karma_service.delete_all_karma(self.karma_member)
        assert self.karma_service.aggregate_member_by_karma(self.karma_member) is None


# Verify that karma messages are identified correctly
class KarmaGiving(unittest.TestCase):
    karma_producer = KarmaProducer(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())

    dummy_wrong_message_content = "lmao <@1>"
    dummy_wrong_message_content_2 = '"thanks dude" <@1>'
    dummy_correct_message_content = "thanks <@1>"
    dummy_correct_message_content_2 = "Thanks <@1>"
    dummy_correct_message_content_3 = "ty <@1>"
    dummy_correct_message_content_4 = "thank You <@1>"

    def test_messages_identified_correctly(self) -> None:
        assert not self.karma_producer.contains_valid_thanks(self.dummy_wrong_message_content)
        assert not self.karma_producer.contains_valid_thanks(self.dummy_wrong_message_content_2)
        assert self.karma_producer.contains_valid_thanks(self.dummy_correct_message_content)
        assert self.karma_producer.contains_valid_thanks(self.dummy_correct_message_content_2)
        assert self.karma_producer.contains_valid_thanks(self.dummy_correct_message_content_3)
        assert self.karma_producer.contains_valid_thanks(self.dummy_correct_message_content_4)
