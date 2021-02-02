from reviewminer.core import *
import pytest


class TestReviewMiner(object):

    def test_one_time_analysis(self):

        reviews_df = pd.read_csv("https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/"
                                 "sample_data/reviews.csv")
        rm = ReviewMiner(reviews_df.head(50), 'id', 'comments')
        assert rm.one_time_analysis(_testing=True) == 1

        rm_empty = ReviewMiner()
        no_df = 0
        try:
            rm_empty.one_time_analysis(_testing=True)
        except AttributeError:
            no_df = 1
        assert no_df == 1
