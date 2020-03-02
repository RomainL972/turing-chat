import unittest
import sys
from gmpy2 import mpz
sys.path.append('../')
import backend

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.turing = backend.TuringChat()
        self.turing.key.key = {
            'n': mpz(285931472310203125690528209113268809453),
            'e': mpz(65537),
            'd': mpz(47575258858455681275057020721522344913)
        }

    def tearDown(self):
        self.turing = None

    def test_parseMessage(self):
        res = self.turing.parseMessage('m a340911b28e27faffbb490c0fad27e29\n')
        self.assertEqual(res, ("message", "salut les amis"))
        res = self.turing.parseMessage("p eyJuIjogImQ3MWM2NjAxM2VhZWU0ODUyZmU3Nzk3ZTRlMmFlZWVkIiwgImUiOiAiMTAwMDEifQ==\n")
        self.assertEqual(res, "pubkey")
        self.assertRaises(ValueError, self.turing.parseMessage, "test salut\n")
        self.assertRaises(ValueError, self.turing.parseMessage, "m -*/456\n")

    def test_createMessage(self):
        self.turing.otherKey = self.turing.key
        self.assertEqual(self.turing.createMessage("message", ""), b"")
        self.assertEqual(
            self.turing.createMessage("message", "salut les amis"),
            b'm a340911b28e27faffbb490c0fad27e29\n'
        )
