import unittest

import mongomock

from core.model.member import KarmaMember
from core.service.karma_service import KarmaService

if __name__ == '__main__':
    unittest.main()


# Verify that karma_services methods are working properly on a mocked mongodb
class KarmaChange(unittest.TestCase):
    def test_karma_increases(self):
        karma_storage = mongomock.MongoClient().db.karma
        karma_service = KarmaService(karma_storage)
        karma_member = KarmaMember('1', '1', '1', '1')
        karma_service.upsert_karma_member(karma_member, True)
        assert karma_service.aggregate_member_by_karma(karma_member) == 1
        karma_service.upsert_karma_member(karma_member, True)
        assert karma_service.aggregate_member_by_karma(karma_member) == 2
        for doc in karma_service.aggregate_member_by_channels(karma_member):
            assert doc['karma'] == 2

    def test_karma_resets(self):
        karma_storage = mongomock.MongoClient().db.karma
        karma_service = KarmaService(karma_storage)
        karma_member = KarmaMember('1', '1', '1', '1')
        karma_service.upsert_karma_member(karma_member, True)
        assert karma_service.aggregate_member_by_karma(karma_member) == 1
        karma_service.delete_all_karma(karma_member.guild_id,
                                       karma_member.member_id)
        assert karma_service.aggregate_member_by_karma(karma_member) is None


# Verify that karma is not given because of running cooldown
class KarmaCooldown(unittest.TestCase):
    def test_karma_not_given(self):
        self.assertEqual(True, False)
