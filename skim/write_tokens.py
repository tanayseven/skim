from pathlib import Path

from skim.types import GroupedTokens


def write_tokens(grouped_tokens: GroupedTokens, path: Path):
    group_length = len(grouped_tokens[0])
    with open(str(path / f'{group_length}.txt'), 'w') as f:
        for group in grouped_tokens:
            f.write(' '.join(group) + '\n')
