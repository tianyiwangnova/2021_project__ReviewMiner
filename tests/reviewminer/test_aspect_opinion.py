from src.reviewminer.aspect_opinion import *
import pandas as pd
import pytest

class TestAspectOpinionExtractor(object):

    sentence = 'Orange juice is healthier than and hot coffee'
    sentence_blob = TextBlob(sentence)
    aoe_null = AspectOpinionExtractor()

    sample_df = pd.DataFrame({
        'id': [123, 134],
        'comment': ['I love drinking orange juice. Orange juice is very healthy. It tastes better than hot coffee.',
                    'I like hot and humid weather in summer. I will usually swim in the river.']})

    def test_aspect_extractor(self):
        assert self.aoe_null.aspect_extractor(self.sentence) == \
               ['orange juice', 'hot coffee', 'coffee']

    def test_valid(self):
        assert self.aoe_null.valid(7, self.sentence_blob) is True
        assert self.aoe_null.valid(8, self.sentence_blob) is False


