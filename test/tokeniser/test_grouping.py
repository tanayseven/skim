import pytest
from collections import namedtuple

from skim.tokeniser import Tokeniser

TokeniserTestCase = namedtuple(
    'TokeniserTestCase', ['input_string', 'groups_of', 'output_group']
)

tokeniser_test_cases = (
    TokeniserTestCase(
        input_string='Empty set of strings should just have',
        groups_of=2,
        output_group=[
            ('<s>', 'Empty'),
            ('Empty', 'set'),
            ('set', 'of'),
            ('of', 'strings'),
            ('strings', 'should'),
            ('should', 'just'),
            ('just', 'have'),
        ],
    ),
    TokeniserTestCase(
        input_string='This is a normal sentence written',
        groups_of=3,
        output_group=[
            ('<s>', 'This', 'is'),
            ('This', 'is', 'a'),
            ('is', 'a', 'normal'),
            ('a', 'normal', 'sentence'),
            ('normal', 'sentence', 'written'),
        ],
    ),
)


@pytest.mark.parametrize(
    'input_string,groups_of,output_group',
    tokeniser_test_cases,
)
def test_tokeniser_grouping(tokeniser: Tokeniser, input_string, groups_of, output_group):
    tokeniser.add_line(input_string)

    assert tokeniser.group_tokens(groups_of=groups_of) == output_group, input_string
