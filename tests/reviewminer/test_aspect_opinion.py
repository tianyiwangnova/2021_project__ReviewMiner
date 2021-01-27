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

    def test_add_word(self):
        sentence1 = 'BUSY residential area with very good restaurants'
        word_list1 = ['busy']
        assert self.aoe_null.add_word(1, word_list1, TextBlob(sentence1)) == ['busy', 'residential']
        assert self.aoe_null.add_word(3, word_list1, TextBlob(sentence1)) == ['busy', 'residential']
        assert self.aoe_null.add_word(4, word_list1, TextBlob(sentence1)) == ['busy', 'residential']

    def test_extract_attributes_pref(self):
        sentence1 = 'Very nice coffee'
        sentence2 = 'nice Brazil coffee'
        sentence3 = "busy residential area"
        assert self.aoe_null.extract_attributes_pref(2, TextBlob(sentence1)) == 'nice'
        assert self.aoe_null.extract_attributes_pref(2, TextBlob(sentence2)) == ''
        assert self.aoe_null.extract_attributes_pref(2, TextBlob(sentence3)) == 'residential busy'

    def test_extract_extract_attributes_suff(self):
        sentence1 = 'The coffee is very delicious'
        sentence2 = 'The coffee is not hot'
        sentence3 = "The weather is COOL"
        assert self.aoe_null.extract_attributes_suff(2, TextBlob(sentence1)) == 'delicious'
        assert self.aoe_null.extract_attributes_suff(2, TextBlob(sentence2)) == 'nothot'
        assert self.aoe_null.extract_attributes_suff(2, TextBlob(sentence3)) == 'cool'

    def test_opinion_extractor(self):
        sentence1 = 'The warm coffee is not hot'
        sentence2 = 'The sunny bedroom is very spacious, with a beautiful wardrobe'
        sentence3 = 'I ate eggs for breakfast'
        assert self.aoe_null.opinion_extractor(['coffee'], TextBlob(sentence1)) == {'coffee': 'warm nothot'}
        assert self.aoe_null.opinion_extractor(['bedroom', 'wardrobe'], TextBlob(sentence2)) == \
                {'bedroom': 'sunny spacious', 'wardrobe': 'beautiful'}
        assert self.aoe_null.opinion_extractor(['eggs'], TextBlob(sentence3)) == {'eggs': ' '}

    def test_aspect_opinion_for_one_comment(self):
        sen = "The sunny bedroom is very spacious, with a beautiful wardrobe"
        assert self.aoe_null.aspect_opinion_for_one_comment(sen) == {'sunny bedroom': ' spacious',
                                                                     'beautiful wardrobe': '',
                                                                     'bedroom': 'sunny spacious',
                                                                     'wardrobe': 'beautiful'}









