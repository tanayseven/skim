# SKIM | Smarter Keyboard Input Method | A simple and smart sentence prediction
# Copyright (C) 2020 Tanay PrabhuDesai

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    TokenizerTestCase(
        case_name="Punctuations are detected as separate tokens",
        input_string="Hi! I want, this done.",
        expected_tokens=["Hi", "!", "I", "want", ",", "this", "done", "."],
    ),
]


@pytest.mark.parametrize("case_name,input_string,expected_tokens", tokenizer_test_cases)
def test_n_grams(case_name, input_string, expected_tokens) -> None:
    # when
    actual_tokens = tokenize(input_string)

    # then
    assert expected_tokens == actual_tokens, case_name
