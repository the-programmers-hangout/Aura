import unittest

import mongomock

from core.model.member import Member
from core.service.karma_service import BlockerService

if __name__ == '__main__':
    unittest.main()


# Verify that member is blacklisted from giving
class MemberIsBlackListed(unittest.TestCase):

    blacklisted = mongomock.MongoClient().db.blacklist
    blocker_service = BlockerService(blacklisted)
    member = Member('1', '1')
    member_2 = Member('1', '2')

    def test_blacklisted_correctly(self):
        self.blocker_service.blacklist(self.member)
        assert self.blocker_service.find_member(self.member) is not None
        assert self.blocker_service.find_member(self.member_2) is None


# Verify that member is whitelisted after being blacklisted
class MemberIsWhiteListed(unittest.TestCase):

    blacklisted = mongomock.MongoClient().db.blacklist
    blocker_service = BlockerService(blacklisted)
    member = Member('1', '1')

    def test_whitelisted_correctly(self):
        self.blocker_service.blacklist(self.member)
        assert self.blocker_service.find_member(self.member) is not None
        self.blocker_service.whitelist(self.member)
        assert self.blocker_service.find_member(self.member) is None
