import unittest

import mongomock

from core.model.member import Member
from core.service.mongo_service import BlockerService, KarmaMemberService

if __name__ == "__main__":
    unittest.main()


# Verify that member is blacklisted from giving karma
class MemberIsBlackListed(unittest.TestCase):
    blocker_source = mongomock.MongoClient().db.blacklist
    blocker_service = BlockerService(blocker_source)
    karma_source = mongomock.MongoClient().db.karma
    karma_service = KarmaMemberService(karma_source)

    member = Member("1", "1")

    def test_member_added_to_blacklist(self):
        self.blocker_service.blacklist(self.member)
        assert self.blocker_service.find_member(self.member) is not None


# Verify that member is whitelisted after being blacklisted
class MemberIsWhiteListed(unittest.TestCase):
    blocker_source = mongomock.MongoClient().db.blacklist
    blocker_service = BlockerService(blocker_source)
    karma_source = mongomock.MongoClient().db.karma
    karma_service = KarmaMemberService(karma_source)

    member = Member("1", "1")

    def test_member_removed_from_blacklist(self):
        self.blocker_service.blacklist(self.member)
        assert self.blocker_service.find_member(self.member) is not None
        self.blocker_service.whitelist(self.member)
        assert self.blocker_service.find_member(self.member) is None
