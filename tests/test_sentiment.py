from reviewminer.sentiment import *
import pandas as pd
import pytest


class TestSentimentScore(object):

    reviews_df = pd.read_csv("https://raw.githubusercontent.com/tianyiwangnova/2021_project__ReviewMiner/main/"
                             "sample_data/reviews.csv")
    ss = SentimentScore(reviews_df.head(100), 'id', 'comments')
    ss1 = SentimentScore(reviews_df.head(100), 'id', 'comments')

    def test_sentiment_for_one_comment(self):
        assert self.ss.sentiment_for_one_comment("I love this bag") == pytest.approx(0.3)
        assert self.ss.sentiment_for_one_comment("The room is not very spacious") == pytest.approx(-0.03)
        assert self.ss.sentiment_for_one_comment("I had dinner") == pytest.approx(0)
        assert self.ss.sentiment_for_one_comment(" ") == pytest.approx(0)

    def test_return_negative_comments(self):
        assert self.ss._return_negative_comments(
            "I had dinner. I love this bag. The room is not very spacious. The lights are terrible") == \
               "The room is not very spacious. The lights are terrible"

    @pytest.mark.mpl_image_compa
    def test_overall_sentiment(self):
        return self.ss.overall_sentiment(_testing=True)

    def test_sentiment_for_one_aspect(self):
        assert round(self.ss.sentiment_for_one_aspect("room"), 4) == pytest.approx(0.4244)
        assert round(self.ss.sentiment_for_one_aspect("host"), 4) == pytest.approx(0.6656)

    def test_aspects_radar_plot(self):
        assert self.ss.aspects_radar_plot(['room', 'place', 'location', 'host', 'neighborhood'], _testing=True) == \
               "plot finished"
        assert self.ss1.aspects_radar_plot(['room', 'place', 'location', 'host', 'neighborhood'], _testing=True) == \
               "plot finished"

    def test_return_all_negative_sentences(self):
        assert len(self.ss.return_all_negative_sentences()) == 23

    def test_negative_comments_by_aspects(self):
        assert len(self.ss.negative_comments_by_aspects()) == 124

    @pytest.mark.mpl_image_compa
    def test_negative_comments_view(self):
        return self.ss.negative_comments_view(_testing=True)

    def test_return_negative_comments_of_aspect(self):
         assert len(self.ss.return_negative_comments_of_aspect('bed')) == 1
         assert len(self.ss1.return_negative_comments_of_aspect('bed')) == 1
         assert len(self.ss.return_negative_comments_of_aspect('abcd')) == 0

