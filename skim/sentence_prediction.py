from pathlib import Path
from typing import List, Dict, Union, Tuple

from skim.n_grams_model import Probability, NGramsModel
from skim.word_to_number_map import Token, WordToNumberMap
from skim.tokenizer import tokenize
from skim.types import WordAsInt


class SentencePrediction:
    def __init__(self, n_grams: int):
        self._n = n_grams
        self._ngrams_model = NGramsModel(n_grams)
        self._word_to_number_map = WordToNumberMap()

    def train(self, input_files: List[Path]):
        for file_path in input_files:
            with open(file_path) as f:
                file_content = f.read()
                tokenized_file_content = tokenize(file_content)
                word_number_list: List[Union[Token, WordAsInt]] = [
                    self._word_to_number_map[word] for word in tokenized_file_content
                ]
                n_grams_chunks = [
                    tuple(word_number_list[i : i + self._n])
                    for i in range(len(word_number_list) - self._n)
                ]
                self._ngrams_model.train(n_grams_chunks)

    def predict(
        self, words: List[Union[Token, WordAsInt]]
    ) -> Tuple[Union[Token, WordAsInt], ...]:
        word_number_list: Tuple[Union[Token, WordAsInt], ...] = tuple(
            self._word_to_number_map[word] for word in words
        )
        predictions = self._ngrams_model.predict(word_number_list)
        return tuple(self._word_to_number_map[prediction] for prediction in predictions)
