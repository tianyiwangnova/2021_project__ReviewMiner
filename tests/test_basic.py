from reviewminer.basic import *
import pandas as pd
import pytest


class TestReviews(object):

    sample_df = pd.DataFrame({
        'id': [123, 134],
        'comment': ['I love drinking orange juice. Orange juice is very healthy. It tastes better than hot coffee.',
                   'I like hot and humid weather in summer. I will usually swim in the river.']})

    def test_data_intake(self):
        sample_review = Reviews(self.sample_df, 'id', 'comment')
        assert sample_review._id_column == 'id', "Expected: 'id'; Actual: {}'".format(sample_review._id_column)
        assert sample_review._review_column == 'comment', "Expected: 'comment'; Actual: {}".format(sample_review.
                                                                                                   _id_column)

    def test_init_special_cases(self):
        sample_review1 = Reviews()
        assert isinstance(sample_review1, Reviews) is True, "Didn't successfully initialize with no inputs"

        sample_review2 = Reviews(self.sample_df)
        assert isinstance(sample_review2, Reviews) is True, "Didn't successfully initialize without id_column & " \
                                                            "review_column"

        id_column_exception = 0
        try:
            sample_review2 = Reviews(self.sample_df, "fake_column1", "comments")
        except ColumnError:
            id_column_exception = 1

        review_column_exception = 0
        try:
            sample_review3 = Reviews(self.sample_df, "id", "fake_column2")
        except ColumnError:
            review_column_exception = 1

        assert id_column_exception == 1
        assert review_column_exception == 1

        df_not_dataframe = 0
        try:
            sample_review4 = Reviews(1, 'id', 'comments')
        except AttributeError:
            df_not_dataframe = 1
        assert df_not_dataframe == 1

    def test_column_setters(self):
        sample_review = Reviews(self.sample_df)
        id_column_exception = 0
        review_column_exception = 0

        try:
            sample_review.id_column = 'abcd'
            sample_review.review_column = 'efgh'
        except ColumnError:
            id_column_exception = 1
            review_column_exception = 1
        assert id_column_exception == 1
        assert review_column_exception == 1

        sample_review.id_column = 'id'
        sample_review.review_column = 'comment'
        sample_review.aspect_mute_list = ['apple', 'PeAr']
        assert sample_review.id_column == 'id'
        assert sample_review.review_column == 'comment'
        assert sample_review.aspect_mute_list == ['apple', 'pear', 'i']

    def test_df_setter(self):
        df_not_dataframe = 0
        try:
            sample_review = Reviews()
            sample_review.df = 1
        except AttributeError:
            df_not_dataframe = 1
        assert df_not_dataframe == 1

    def test_aspect_mute_list_setter(self):
        aspect_mute_list_wrong = 0
        try:
            sample_review = Reviews()
            sample_review.aspect_mute_list = 1
        except AttributeError:
            aspect_mute_list_wrong = 1
        assert aspect_mute_list_wrong == 1








