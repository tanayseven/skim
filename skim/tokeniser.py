import re


class Tokeniser:
    def __init__(self):
        self._tokens = ['<s>']

    def add_line(self, line: str):
        separated_punctuations = (_separate_punctuations_from_words(line) + ' \n')
        self._tokens.extend(separated_punctuations.split(' '))
        self._tokens = [token for token in self._tokens if token != '']

    @property
    def tokens(self):
        return self._tokens


PUNCTUATIONS = (
    '.',
    ',',
    '?',
    '!',
)

REPLACEMENT_DICT = {
    re.escape(elem): (' ' + elem)
    for elem in PUNCTUATIONS
}

PATTERN = re.compile('|'.join(REPLACEMENT_DICT.keys()))


def _separate_punctuations_from_words(line: str) -> str:
    return PATTERN.sub(lambda m: REPLACEMENT_DICT[re.escape(m.group(0))], line)
