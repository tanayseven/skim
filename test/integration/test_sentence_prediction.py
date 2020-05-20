from pathlib import Path

import pytest

from skim.sentence_prediction import SentencePrediction


@pytest.fixture(scope="module")
def trained_model():
    sentence_prediction = SentencePrediction(n_grams=3)
    sentence_prediction.train([Path("test/integration/sample_input_file.txt")])
    return sentence_prediction


def test_sentence_prediction(trained_model: SentencePrediction):
    predictions = trained_model.predict(("writing", "this"))

    assert predictions == ("email", "message", "program")
