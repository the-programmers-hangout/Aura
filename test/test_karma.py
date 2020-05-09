import unittest

if __name__ == '__main__':
    unittest.main()


# Verify that karma is given through all the possible permutations
class KarmaGiven(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


# Verify that karma is not given because of running cooldown
class KarmaCooldown(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)
