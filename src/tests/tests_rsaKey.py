import unittest
import sys
sys.path.append('../')
import backend
from gmpy2 import mpz

class TestRSAKey(unittest.TestCase):
    def setUp(self):
        self.key = backend.RSAKey()
        self.key.key = {
            'n': mpz(285931472310203125690528209113268809453),
            'e': mpz(65537),
            'd': mpz(47575258858455681275057020721522344913)
        }

    def tearDown(self):
        self.key = None

    def test_encrypt(self):
        self.assertEqual(
            self.key.encrypt("salut"),
            b"98d93969a1426d713fdae794f036bfe1"
        )

    def test_decrypt(self):
        self.assertEqual(
            self.key.decrypt(b'1274da0d802d1f9c502caed2b49020c6'),
            "test456"
        )

    def test_generate(self):
        key = backend.RSAKey()
        key.generate(256)
        self.assertEqual(key.decrypt(key.encrypt("this is a test")), "this is a test")

    def test_toJson(self):
        self.assertEqual(self.key.toJson(), '{"n": "d71c66013eaee4852fe7797e4e2aeeed", "e": "10001", "d": "23caa95c4eaa3a02730f965a8a3903d1"}')

    def test_fromJson(self):
        key = backend.RSAKey()
        key.fromJson('{"n": "4a24d84af012eb52aa3083dbba89bcf5", "e": "10001", "d": "11e06f5c262551a2a2e071f98bfaf903"}')
        self.assertEqual(key.key, {'n': mpz(98554181312648717508777189852108668149), 'e': mpz(65537), 'd': mpz(23762209072917874016222680172199606531)})

    def test_getPublicKey(self):
        pubkey = self.key.getPublicKey()
        self.assertEqual(self.key.key["n"], pubkey.key["n"])
        self.assertEqual(self.key.key["e"], pubkey.key["e"])
        self.assertFalse("d" in pubkey.key)

    def test_toBase64(self):
        self.assertEqual(self.key.toBase64(), b"eyJuIjogImQ3MWM2NjAxM2VhZWU0ODUyZmU3Nzk3ZTRlMmFlZWVkIiwgImUiOiAiMTAwMDEiLCAiZCI6ICIyM2NhYTk1YzRlYWEzYTAyNzMwZjk2NWE4YTM5MDNkMSJ9")

    def test_fromBase64(self):
        key = backend.RSAKey()
        key.fromBase64("eyJuIjogImQ3MWM2NjAxM2VhZWU0ODUyZmU3Nzk3ZTRlMmFlZWVkIiwgImUiOiAiMTAwMDEiLCAiZCI6ICIyM2NhYTk1YzRlYWEzYTAyNzMwZjk2NWE4YTM5MDNkMSJ9")
        self.assertEqual(key.key, self.key.key)

if __name__ == '__main__':
    unittest.main()
