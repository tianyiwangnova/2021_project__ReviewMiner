from src.reviewminer.aspect_opinion import *
import pandas as pd
import pytest

class TestAspectOpinionExtractor(object):

    sentence = 'Orange juice is healthier than and hot coffee'
    sentence_blob = TextBlob(sentence)
    aoe_null = AspectOpinionExtractor()
    aspect_dict = "{'building':'tall beautiful magnificent', 'music':'classic pop calm'}"

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

    def test_merge_two_dicts(self):
        dict1 = {'a': 'apple', 'b': 'boy'}
        dict2 = {'a': 'air', 'c': 'cat'}
        assert self.aoe_null.merge_two_dicts(dict1, dict2) == {'a': 'apple air', 'b': 'boy', 'c': 'cat'}

    def test_has_aspect(self):
        assert self.aoe_null.has_aspect(self.aspect_dict, 'building') is True
        assert self.aoe_null.has_aspect(self.aspect_dict, 'tall') is False

    def test_has_opinion(self):
        assert self.aoe_null.has_opinion(self.aspect_dict, 'building', 'beautiful') is True
        assert self.aoe_null.has_opinion(self.aspect_dict, 'music', 'beautiful') is False

    def test_is_be(self):
        assert self.aoe_null.is_be(2, self.sentence_blob) is True
        assert self.aoe_null.is_be(10, self.sentence_blob) is False
        assert self.aoe_null.is_be(1, self.sentence_blob) is False







