from pathlib import Path
from typing import List, Dict, Union, Tuple, Optional

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
            with file_path.open(mode="r") as f:
                file_content = f.read()
            tokenized_file_content = tokenize(file_content)
            word_number_list: List[WordAsInt] = [
                self._word_to_number_map.add_word(word)
                for word in tokenized_file_content
            ]
            n_grams_chunks: List[Tuple[WordAsInt, ...]] = [
                tuple(word_number_list[i : i + self._n])
                for i in range(len(word_number_list) - self._n)
            ]
            self._ngrams_model.train(n_grams_chunks)

    def predict(self, words: List[Token]) -> Optional[Tuple[Token, ...]]:
        word_number_list: Tuple[WordAsInt, ...] = tuple()
        for word in words:
            if self._word_to_number_map.number_for_word(word) is None:
                return None
            word_number_list += (self._word_to_number_map.number_for_word(word),)
        predictions = self._ngrams_model.predict(word_number_list)
        resultant_list: Tuple[Token, ...] = tuple()
        for prediction in predictions:
            resultant_list += (self._word_to_number_map.word_for_number(prediction),)
        return resultant_list
