import unittest

import mongomock

from core.model.member import Member
from core.service.karma_service import BlockerService

if __name__ == '__main__':
    unittest.main()


# Verify that member is blacklisted from giving
class MemberIsBlackListed(unittest.TestCase):
    def test_blacklisted_correctly(self):
        blacklisted = mongomock.MongoClient().db.blacklist
        blocker_service = BlockerService(blacklisted)
        member = Member('1', '1')
        member_2 = Member('1', '2')
        blocker_service.blacklist(member)
        assert blocker_service.find_member(member) is not None
        assert blocker_service.find_member(member_2) is None


# Verify that member is whitelisted after being blacklisted
class MemberIsWhiteListed(unittest.TestCase):
    def test_whitelisted_correctly(self):
        blacklisted = mongomock.MongoClient().db.blacklist
        blocker_service = BlockerService(blacklisted)
        member = Member('1', '1')
        blocker_service.blacklist(member)
        assert blocker_service.find_member(member) is not None
        blocker_service.whitelist(member)
        assert blocker_service.find_member(member) is None
