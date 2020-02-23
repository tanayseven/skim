from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from skim.types import GroupedTokens
from skim.raw_file import write_tokens, load_raw_text


def test_write_token():
    grouped_tokens_2: GroupedTokens = [
        ('<s>', 'The'),
        ('The', 'man'),
    ]
    grouped_tokens_3: GroupedTokens = [
        ('<s>', 'The', 'man'),
        ('The', 'man', 'ran'),
    ]
    expected_grouped_token_2_file_content = '''<s> The\nThe man\n'''
    expected_grouped_token_3_file_content = '''<s> The man\nThe man ran\n'''
    with TemporaryDirectory() as temp_directory:
        temp_dir_path = Path(temp_directory)
        write_tokens(grouped_tokens_2, temp_dir_path)
        write_tokens(grouped_tokens_3, temp_dir_path)
        with open(temp_dir_path / '2.txt') as f:
            actual_grouped_token_2_file_content = f.read()
        with open(temp_dir_path / '3.txt') as f:
            actual_grouped_token_3_file_content = f.read()
        assert actual_grouped_token_2_file_content == expected_grouped_token_2_file_content
        assert actual_grouped_token_3_file_content == expected_grouped_token_3_file_content


def test_read_raw_file():
    expected_grouped_tokens = [
        ('The', 'man'),
        ('man', 'ran'),
        ('ran', 'really'),
        ('really', 'fast'),
        ('This', 'is'),
        ('is', 'a'),
        ('a', 'really'),
        ('really', 'good'),
        ('good', 'text'),
    ]
    with TemporaryDirectory() as temp_directory:
        temp_directory = Path(temp_directory)
        with open(temp_directory / 'sample_1.txt', 'w') as f:
            f.write('The man ran really fast')
        with open(temp_directory / 'sample_2.txt', 'w') as f:
            f.write('This is a really good text')
        tokeniser = load_raw_text(temp_directory)
        actual_grouped_tokens = tokeniser.group_tokens(2)
        print(f'Actual: {actual_grouped_tokens}')
        print(f'Actual: {expected_grouped_tokens}')
        assert set(expected_grouped_tokens).issubset(set(actual_grouped_tokens))
