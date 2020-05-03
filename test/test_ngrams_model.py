from collections import namedtuple

import pytest

from skim.exceptions import ModelNotTrainedException
from skim.n_grams_model import NGramsModel

NGramsTestCase = namedtuple('NGramsTestCase', ["case_name", "training_set", "prediction_input", "prediction_outcome"])

n_grams_test_cases = [
    NGramsTestCase(
        case_name="Simple two words bi-gram",
        training_set=[
            (0, 1),
        ],
        prediction_input=(0,),
        prediction_outcome=(1,),
    ),
    NGramsTestCase(
        case_name="Bi-grams with equal probabilities",
        training_set=[
            (0, 1),
            (0, 2),
        ],
        prediction_input=(0,),
        prediction_outcome=(1, 2),
    ),
    NGramsTestCase(
        case_name="Bi-grams with one probability higher than other",
        training_set=[
            (0, 1),
            (0, 2),
            (0, 2),
        ],
        prediction_input=(0,),
        prediction_outcome=(2, 1),
    ),
    NGramsTestCase(
        case_name="Bi-grams with three different probabilities",
        training_set=[
            (0, 1),
            (0, 2),
            (0, 2),
            (0, 2),
            (0, 3),
            (0, 3),
        ],
        prediction_input=(0,),
        prediction_outcome=(2, 3, 1),
    ),
    NGramsTestCase(
        case_name="Tri-grams with three different probabilities",
        training_set=[
            (0, 6, 1),
            (0, 6, 2),
            (0, 6, 2),
            (0, 6, 2),
            (0, 6, 3),
            (0, 6, 3),
            (0, 7, 1),
            (5, 6, 8),
        ],
        prediction_input=(0, 6),
        prediction_outcome=(2, 3, 1),
    ),
]


@pytest.mark.parametrize("case_name,training_set,prediction_input,prediction_outcome", n_grams_test_cases)
def test_n_grams(case_name, training_set, prediction_input, prediction_outcome) -> None:
    # given
    n_grams_model = NGramsModel()
    n_grams_model.train(training_set)
    expected_prediction = prediction_outcome

    # when
    actual_prediction = n_grams_model.predict(prediction_input)

    # then
    assert expected_prediction == actual_prediction, case_name


def test_untrained_model_throws_exception_while_predicting() -> None:
    # given
    n_grams_model = NGramsModel()

    with pytest.raises(ModelNotTrainedException):
        n_grams_model.predict((0,))
