import unittest

if __name__ == '__main__':
    unittest.main()


# Verify that member is blacklisted from giving
class MemberIsBlackListed(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


# Verify that member is whitelisted after being blacklisted
class MemberIsWhiteListed(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)
