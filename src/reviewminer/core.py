class Reviews:
    """
    Information about the reviews data
    """

    def __init__(self,
                 df=None,
                 id_column=None,
                 review_column=None):
        """
        Take a data frame where each row is a comment/review

        :param df: a data frame where each row is a comment/review; The data frame should have at least an ID column
                   that stores the unique IDs of the comments, and a review column where the actual comments/reviews
                   are stored
        :param id_column: the name of the column that stores the unique IDs of the comments
        :param review_column: the name of the column where the actual comments/reviews are stored
        """
        self.df = df
        self.id_column = id_column
        self.review_column = review_column


class AspectOpinionExtractor(Reviews):
    def __init__(self,
                 df=None,
                 id_column=None,
                 review_column=None):
        """
        Take a data frame where each row is a comment/review

        :param df: a data frame where each row is a comment/review; The data frame should have at least an ID column
                   that stores the unique IDs of the comments, and a review column where the actual comments/reviews
                   are stored
        :param id_column: the name of the column that stores the unique IDs of the comments
        :param review_column: the name of the column where the actual comments/reviews are stored
        """
        Reviews.__init__(self, df, id_column, review_column)
