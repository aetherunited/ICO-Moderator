from unittest import TestCase

from commands import qa


class TestQuestionUtils(TestCase):

    def test_is_question(self):
        self.assertEqual(qa.is_question('What is Aether United?'), 'what')
        self.assertEqual(qa.is_question('Where is the moon?'), 'where')
        self.assertEqual(qa.is_question('How do you buy Ethereum?'), 'how')
        self.assertEqual(qa.is_question('I like dogs.'), False)
        self.assertEqual(qa.is_question('This is a cat.'), False)
        self.assertEqual(qa.is_question("what's aun?"), 'what')
        self.assertEqual(qa.is_question("what's aun"), 'what')
        self.assertEqual(qa.is_question("whats aun"), 'what')
        self.assertEqual(qa.is_question("This is how it's done."), False)
        self.assertEqual(qa.is_question('this is how its done'), False)

    def test_contains_question(self):
        self.assertEqual(qa.contains_question("Here is your dinner. What's the magic word?"), ("What's the magic word?", 'what'))
        self.assertEqual(qa.contains_question('What is ETH?'), ('What is ETH?', 'what'))
        self.assertEqual(qa.contains_question('Where is ETH?'), ('Where is ETH?', 'where'))
        self.assertEqual(qa.contains_question('Here we go. Time to do things.'), (False, None))
        self.assertEqual(qa.contains_question('its k bb. sall guud.'), (False, None))

    def test_match_subject(self):
        self.assertEqual(qa.match_subject('how do i invest in aether')[0], 'invest-aether-united')
        self.assertEqual(qa.match_subject('who runs aun')[0], 'runs-aether-united')
        self.assertEqual(qa.match_subject('how do i join aether')[0], 'join-aether-united')
        self.assertEqual(qa.match_subject('where do i join aether')[0], 'join-aether-united')
        self.assertEqual(qa.match_subject('what is blockchain')[0], 'blockchain')
        self.assertEqual(qa.match_subject('how does blockchain work')[0], 'blockchain-explanation')
