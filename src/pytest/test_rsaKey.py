import pytest
import sys
import os
from gmpy2 import mpz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import backend


@pytest.fixture
def rsa_key():
    key = backend.RSAKey()
    key.key = {
        'n': mpz(285931472310203125690528209113268809453),
        'e': mpz(65537),
        'd': mpz(47575258858455681275057020721522344913)
    }
    return key


@pytest.fixture
def empty_rsa_key():
    return backend.RSAKey()


def test_encrypt(rsa_key):
    assert rsa_key.encrypt("salut") == b"98d93969a1426d713fdae794f036bfe1"


def test_decrypt(rsa_key):
    assert rsa_key.decrypt(b'1274da0d802d1f9c502caed2b49020c6') == "test456"


def test_generate():
    key = backend.RSAKey()
    key.generate(256)
    assert key.decrypt(key.encrypt("this is a test")) == "this is a test"


def test_toJson(rsa_key):
    assert rsa_key.toJson() == '{"n": "d71c66013eaee4852fe7797e4e2aeeed", \
"e": "10001", "d": "23caa95c4eaa3a02730f965a8a3903d1"}'


def test_fromJson(empty_rsa_key):
    empty_rsa_key.fromJson('{"n": "4a24d84af012eb52aa3083dbba89bcf5", "e": "10001", "d": "11e06f5c262551a2a2e071f98bfaf903"}')
    assert empty_rsa_key.key == {
        'n': mpz(98554181312648717508777189852108668149),
        'e': mpz(65537),
        'd': mpz(23762209072917874016222680172199606531)
    }


def test_getPublicKey(rsa_key):
    pubkey = rsa_key.getPublicKey()
    assert rsa_key.key["n"] == pubkey.key["n"]
    assert rsa_key.key["e"] == pubkey.key["e"]
    assert "d" not in pubkey.key


def test_toBase64(rsa_key):
    assert rsa_key.toBase64() == b"eyJuIjogImQ3MWM2NjAxM2VhZWU0ODUyZmU3Nzk3ZTRl\
MmFlZWVkIiwgImUiOiAiMTAwMDEiLCAiZCI6ICIyM2NhYTk1YzRlYWEzYTAyNzMwZjk2NWE4YTM5MDNkMSJ9"


def test_fromBase64(rsa_key, empty_rsa_key):
    empty_rsa_key.fromBase64("eyJuIjogImQ3MWM2NjAxM2VhZWU0ODUyZmU3Nzk3ZTRlMmFlZ\
WVkIiwgImUiOiAiMTAwMDEiLCAiZCI6ICIyM2NhYTk1YzRlYWEzYTAyNzMwZjk2NWE4YTM5MDNkMSJ9")
    assert empty_rsa_key.key == rsa_key.key

def test_getFingerprint(rsa_key, empty_rsa_key):
    assert empty_rsa_key.getFingerprint() == ''
    assert rsa_key.getFingerprint() == "2d:d5:66:ed:70:88:53:cb:4f:f5:1e:ed:25:76:b7:e9"
