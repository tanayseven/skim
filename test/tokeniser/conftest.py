import pytest

from skim.tokeniser import Tokeniser

@pytest.fixture
def tokeniser():
    yield Tokeniser()
