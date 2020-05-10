import unittest

import mongomock

from cogs.karma.producer import KarmaProducer
from core.model.member import KarmaMember
from core.service.karma_service import KarmaService

if __name__ == '__main__':
    unittest.main()


# Verify that karma is given through all the possible permutations
class KarmaChange(unittest.TestCase):
    def test_karma_increases(self):
        karma_storage = mongomock.MongoClient().db.karma
        karma_service = KarmaService(karma_storage)
        karma_member = KarmaMember('1', '1', '1', '1')
        karma_service.upsert_karma_member(karma_member, True)
        assert karma_service.aggregate_member_by_karma(karma_member) == 1
        karma_service.upsert_karma_member(karma_member, True)
        assert karma_service.aggregate_member_by_karma(karma_member) == 2


# Verify that karma is not given because of running cooldown
class KarmaCooldown(unittest.TestCase):
    def test_karma_not_given(self):
        self.assertEqual(True, False)
