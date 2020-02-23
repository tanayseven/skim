import pytest
from collections import namedtuple

from skim.tokeniser import Tokeniser

TokeniserTestCase = namedtuple(
    'TokeniserTestCase', ['case_name', 'input_string', 'output_list']
)

tokeniser_test_cases = (
    TokeniserTestCase(
        case_name='Empty set of strings should just have <s>',
        input_string='',
        output_list=['<s>', '\n'],
    ),
    TokeniserTestCase(
        case_name='A single line of three tokens',
        input_string='I am Sam',
        output_list=['<s>', 'I', 'am', 'Sam', '\n'],
    ),
    TokeniserTestCase(
        case_name='Multiple sentence should have full stops tokenised',
        input_string='I am Sam. Sam I am.',
        output_list=['<s>', 'I', 'am', 'Sam', '.', 'Sam', 'I', 'am', '.', '\n'],
    ),
    TokeniserTestCase(
        case_name='Question sentense',
        input_string='Hello, how are you doing?',
        output_list=['<s>', 'Hello', ',', 'how', 'are', 'you', 'doing', '?', '\n'],
    ),
)


@pytest.mark.parametrize(
    'case_name,input_string,output_list',
    tokeniser_test_cases,
)
def test_parameterized_tokeniser(tokeniser: Tokeniser, case_name, input_string, output_list):
    tokeniser.add_line(input_string)

    assert tokeniser.tokens == output_list, case_name
