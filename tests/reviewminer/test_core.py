from src.reviewminer.core import *
import pandas as pd
import pytest


class TestReviews(object):

    sample_df = pd.DataFrame({
        'id':[123, 134, 145],
        'comment':['I love drinking orange juice. Orange juice is very healthy. It tastes better than hot coffee.',
                   'I like hot and humid weather in summer. I will usually swim in the river.']})

    def test_data_intake(self):
        sample_review = Reviews(sample_df, 'id', 'comment')
        assert sample_review.id_column == 'id', "Expected: 'id'; Actual: {}".format(sample_review.id_column)

