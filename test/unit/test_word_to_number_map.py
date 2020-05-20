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

from skim.word_to_number_map import WordToNumberMap

WordToNumberMapTestCase = namedtuple(
    "WordToNumberMapTestCase",
    ["case_name", "add_words", "remove_words", "expected_number_map"],
)

word_to_number_map_test_cases = [
    WordToNumberMapTestCase(
        case_name="Simple two words",
        add_words=["This", "word"],
        remove_words=[],
        expected_number_map={"This": 0, "word": 1},
    ),
    WordToNumberMapTestCase(
        case_name="Simple three words",
        add_words=["This", "words", "rock"],
        remove_words=[],
        expected_number_map={"This": 0, "words": 1, "rock": 2},
    ),
    WordToNumberMapTestCase(
        case_name="Add three words and remove the middle word",
        add_words=["This", "words", "rock"],
        remove_words=["words"],
        expected_number_map={"This": 0, "words": 3, "rock": 2},
    ),
]


@pytest.mark.parametrize(
    "case_name,add_words,remove_words,expected_number_map",
    word_to_number_map_test_cases,
)
def test_word_prediction_model(case_name, add_words, remove_words, expected_number_map):
    # given
    word_to_number_map = WordToNumberMap()

    # when
    _ = [word_to_number_map[word] for word in add_words]
    for word in remove_words:
        del word_to_number_map[word]

    # then
    assert all(
        [word_to_number_map[key] == value for key, value in expected_number_map.items()]
    ), case_name
    assert all(
        [word_to_number_map[value] == key for key, value in expected_number_map.items()]
    ), case_name
