from glob import glob
from pathlib import Path

from skim.tokeniser import Tokeniser
from skim.types import GroupedTokens


def write_tokens(grouped_tokens: GroupedTokens, dir_path: Path):
    group_length = len(grouped_tokens[0])
    with open(str(dir_path / f'{group_length}.txt'), 'w') as f:
        for group in grouped_tokens:
            f.write(' '.join(group) + '\n')


def load_raw_text(dir_path: Path) -> Tokeniser:
    raw_files = [file for file in glob(f'{str(dir_path)}/**/*txt', recursive=True)]
    tokeniser = Tokeniser()
    for file in raw_files:
        with open(str(file)) as f:
            for line in f.readlines():
                tokeniser.add_line(line)
    return tokeniser
