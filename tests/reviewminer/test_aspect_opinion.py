from src.reviewminer.aspect_opinion import *
import pandas as pd
import pytest

class TestAspectOpinionExtractor(object):

    sample_df = pd.DataFrame({
        'id': [123, 134],
        'comment': ['I love drinking orange juice. Orange juice is very healthy. It tastes better than hot coffee.',
                    'I like hot and humid weather in summer. I will usually swim in the river.']})

    def test_aspect_extractor(self):
        aoe = AspectOpinionExtractor()
        assert aoe.aspect_extractor("Orange juice is healthier than and hot coffee") == \
               ['orange juice', 'hot coffee', 'coffee']


