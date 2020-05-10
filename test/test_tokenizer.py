from collections import namedtuple

import pytest

from skim.tokenizer import tokenize

TokenizerTestCase = namedtuple(
    "TokenizerTestCase", ["case_name", "input_string", "expected_tokens"],
)

tokenizer_test_cases = [
    TokenizerTestCase(
        case_name="Empty string given as input", input_string="", expected_tokens=[]
    ),
    TokenizerTestCase(
        case_name="A simple string with two words",
        input_string="This word",
        expected_tokens=["This", "word"],
    ),
    TokenizerTestCase(
        case_name="A simple string with tab instead of a space",
        input_string="This\tword",
        expected_tokens=["This", "word"],
    ),
    TokenizerTestCase(
        case_name="A string in Devanagri script",
        input_string="काळा बाळ",
        expected_tokens=["काळा", "बाळ"],
    ),
]


@pytest.mark.parametrize("case_name,input_string,expected_tokens", tokenizer_test_cases)
def test_n_grams(case_name, input_string, expected_tokens) -> None:
    # when
    actual_tokens = tokenize(input_string)

    # then
    assert expected_tokens == actual_tokens, case_name
