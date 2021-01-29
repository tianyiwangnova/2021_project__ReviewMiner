from src.reviewminer.sentiment import *


class ReviewMiner(SentimentScore):

    def __init__(self,
                 df: pd.DataFrame = None,
                 id_column: str = None,
                 review_column: str = None):
        """
        Take a data frame where each row is a comment/review

        :param df: a data frame where each row is a comment/review; The data frame should have at least an ID column
                   that stores the unique IDs of the comments, and a review column where the actual comments/reviews
                   are stored
        :param id_column: the name of the column that stores the unique IDs of the comments
        :param review_column: the name of the column where the actual comments/reviews are stored
        """
        SentimentScore.__init__(self, df=df, id_column=id_column, review_column=review_column)

    def one_time_analysis(self):

        try:
            if not isinstance(self.df, pd.DataFrame):
                raise AttributeError("`df`(the review data) should be a pandas DataFrame")
        except AttributeError:
            print("Please assign your review data to the class by `ReviewMiner.df = <your df>`, " \
                  "The table should be a pandas DataFrame. Please specify the id_column and review_" \
                  "column too")





