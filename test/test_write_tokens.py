from pathlib import Path
from tempfile import TemporaryDirectory

from skim.types import GroupedTokens
from skim.write_tokens import write_tokens


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
