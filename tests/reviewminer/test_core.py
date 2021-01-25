from src.reviewminer.core import *
import pandas as pd
import pytest

class TestReviews(object):

    sample_df = pd.DataFrame({
        'id': [123, 134],
        'comment': ['I love drinking orange juice. Orange juice is very healthy. It tastes better than hot coffee.',
                   'I like hot and humid weather in summer. I will usually swim in the river.']})

    def test_data_intake(self):
        sample_review = Reviews(self.sample_df, 'id', 'comment')
        assert sample_review.id_column == 'id', "Expected: 'id'; Actual: {}'".format(sample_review.id_column)
        assert sample_review.review_column == 'comment', "Expected: 'comment'; Actual: {}".format(sample_review.id_column)

    def test_init_special_cases(self):
        sample_review1 = Reviews()
        assert isinstance(sample_review1, Reviews) is True, "Didn't successfully initialize with no inputs"

        sample_review2 = Reviews(self.sample_df)
        assert isinstance(sample_review2, Reviews) is True, "Didn't successfully initialize without id_column & " \
                                                            "review_column"

        id_column_exception = 0
        review_column_exception = 0
        try:
            sample_review2 = Reviews(self.sample_df, "fake_column1", "fake_column2")
        except ColumnError:
            id_column_exception = 1
            review_column_exception = 1
        assert id_column_exception == 1
        assert review_column_exception == 1


# class TestAspectOpinionExtractor(object):
#
#     sample_df = pd.DataFrame({
#         'id': [123, 134],
#         'comment': ['I love drinking orange juice. Orange juice is very healthy. It tastes better than hot coffee.',
#                     'I like hot and humid weather in summer. I will usually swim in the river.']})
#
#     def test_aspect_extractor(self):






