import pytest
import sys
import os
from gmpy2 import mpz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import backend


@pytest.fixture
def turing():
    turing = backend.TuringChat(False)
    turing.key.key = {
        'n': mpz(285931472310203125690528209113268809453),
        'e': mpz(65537),
        'd': mpz(47575258858455681275057020721522344913)
    }
    return turing


def test_parseMessage(turing):
    assert turing.parseMessage('m a340911b28e27faffbb490c0fad27e29\n') == ("message", "salut les amis")
    assert turing.parseMessage("p eyJuIjogImQ3MWM2NjAxM2VhZWU0ODUyZmU3Nzk3ZTRlMmFlZWVkIiwgImUiOiAiMTAwMDEifQ==\n") == ("pubkey", '\
2d:d5:66:ed:70:88:53:cb:4f:f5:1e:ed:25:76:b7:e9')
    with pytest.raises(ValueError):
        turing.parseMessage("test salut\n")
    with pytest.raises(ValueError):
        turing.parseMessage("m -*/456\n")


def test_createMessage(turing):
    turing.otherKey = turing.key
    assert turing.createMessage("message", "") == b""
    assert turing.createMessage("message", "salut les amis") == b'm a340911b28e27faffbb490c0fad27e29\n'
