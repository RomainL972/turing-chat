import pytest
import sys
import os
from gmpy2 import mpz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rsa

@pytest.fixture
def rsa_key():
    return {
        'n': mpz(285931472310203125690528209113268809453),
        'e': mpz(65537),
        'd': mpz(47575258858455681275057020721522344913)
    }

def test_encrypt(rsa_key):
    assert rsa.encrypt("abcd",rsa_key["e"],rsa_key["n"]) == 'b8f2c1456e5d44b0762bdb489298c399'

def test_decrypt(rsa_key):
    assert rsa.decrypt("b8f2c1456e5d44b0762bdb489298c399", rsa_key["d"], rsa_key["n"])

def test_genKey():
    key = rsa.genKey(256)
    assert "1234defa" == rsa.decrypt(rsa.encrypt("1234defa", key["e"], key["n"]), key["d"], key["n"])
