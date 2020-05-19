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

from typing import List, Tuple, Dict, Optional, NewType

from skim.exceptions import ModelNotTrainedException

OccurrenceCount = NewType("OccurrenceCount", int)
PossiblePrediction = NewType("PossiblePrediction", int)
Probability = NewType("Probability", float)
NGramsKey = Tuple[OccurrenceCount, ...]
Prediction = Dict[PossiblePrediction, Probability]
NGramsProbabilityMap = Dict[NGramsKey, Prediction]
NGramsCountMap = Dict[NGramsKey, OccurrenceCount]
TrainingSet = List[NGramsKey]


class NGramsModel:
    def __init__(self, n: int = 10) -> None:
        self._probability_map: Optional[Dict[NGramsKey, Prediction]] = None
        self._n = n

    def train(self, training_set: List[NGramsKey]) -> None:
        n_count_map = count_n_gram_sequences(training_set)
        n_minus_one_map = count_n_gram_sequences(
            training_set, should_count_n_minus_one=True
        )
        probability_map = compute_n_grams_probabilities(n_count_map, n_minus_one_map)
        self._probability_map = probability_map

    def predict(
        self, test_sequence: NGramsKey, max_predictions=3
    ) -> Tuple[PossiblePrediction, ...]:
        if self._probability_map is None:
            raise ModelNotTrainedException
        predictions = self._probability_map[test_sequence]
        return tuple(
            sorted(
                predictions,
                key=lambda possible_prediction: predictions[possible_prediction],
                reverse=True,
            )[:max_predictions]
        )


def count_n_gram_sequences(
    training_set: TrainingSet, should_count_n_minus_one=False
) -> NGramsCountMap:
    n_count_map: NGramsCountMap = {}
    for training_sequence in training_set:
        key = training_sequence[:-1] if should_count_n_minus_one else training_sequence
        try:
            n_count_map[key] = OccurrenceCount(n_count_map[key] + OccurrenceCount(1))
        except KeyError:
            n_count_map[key] = OccurrenceCount(1)
    return n_count_map


def compute_n_grams_probabilities(
    n_count_map: NGramsCountMap, n_minus_one_map: NGramsCountMap
) -> NGramsProbabilityMap:
    probability_map: NGramsProbabilityMap = {}
    for n_count_key in n_count_map.keys():
        n_minus_one_count_key = n_count_key[:-1]
        possible_prediction = PossiblePrediction(n_count_key[-1])
        probability = Probability(
            n_count_map[n_count_key] / n_minus_one_map[n_minus_one_count_key]
        )
        try:
            probability_map[n_minus_one_count_key][possible_prediction] = probability
        except KeyError:
            probability_map[n_minus_one_count_key] = {possible_prediction: probability}
    return probability_map
