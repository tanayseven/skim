from typing import List, Tuple, Dict, Optional, NewType

from skim.exceptions import ModelNotTrainedException

OccurrenceCount = NewType('OccurrenceCount', int)
PossiblePrediction = NewType("PossiblePrediction", int)
Probability = NewType("Probability", float)
NGramsKey = Tuple[OccurrenceCount, ...]
Prediction = Dict[PossiblePrediction, Probability]


class NGramsModel:

    def __init__(self, n: int = 10) -> None:
        self._probability_map: Optional[Dict[NGramsKey, Prediction]] = None
        self._n = n

    def train(self, training_set: List[NGramsKey]) -> None:
        n_count_map: Dict[NGramsKey, OccurrenceCount] = {}
        n_minus_one_map: Dict[NGramsKey, OccurrenceCount] = {}
        for training_sequence in training_set:
            try:
                n_count_map[training_sequence] += 1
            except KeyError:
                n_count_map[training_sequence] = OccurrenceCount(1)
            n_minus_one = training_sequence[:-1]
            try:
                n_minus_one_map[n_minus_one] += 1
            except KeyError:
                n_minus_one_map[n_minus_one] = OccurrenceCount(1)
        probability_map: Dict[NGramsKey, Prediction] = {}
        for n_count_key in n_count_map.keys():
            n_minus_one_count_key = n_count_key[:-1]
            possible_prediction = PossiblePrediction(n_count_key[-1])
            probability = Probability(n_count_map[n_count_key] / n_minus_one_map[n_minus_one_count_key])
            try:
                probability_map[n_minus_one_count_key][possible_prediction] = probability
            except KeyError:
                probability_map[n_minus_one_count_key] = {possible_prediction: probability}
        self._probability_map = probability_map

    def predict(self, test_sequence: NGramsKey, max_predictions=3) -> Tuple[PossiblePrediction]:
        if self._probability_map is None:
            raise ModelNotTrainedException
        predictions = self._probability_map[test_sequence]
        return tuple(sorted(
            predictions,
            key=lambda possible_prediction: predictions[possible_prediction],
            reverse=True,
        )[:max_predictions])
