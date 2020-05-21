from pathlib import Path

import pytest

from skim.sentence_prediction import SentencePrediction


@pytest.fixture(scope="module")
def trained_model():
    sentence_prediction = SentencePrediction(n_grams=3)
    sentence_prediction.train([Path("test/integration/sample_input_file.txt")])
    return sentence_prediction


def test_for_valid_input(trained_model: SentencePrediction):
    predictions = trained_model.predict(("writing", "this"))

    assert predictions == ("email", "message", "program")


def test_for_invalid_input(trained_model: SentencePrediction):
    predictions = trained_model.predict(("writing", "random_word"))

    assert predictions is None
