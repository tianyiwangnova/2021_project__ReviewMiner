import pandas as pd


class ColumnError(Exception):
    pass


class Reviews:
    """
    Information about the reviews data
    """

    def __init__(self,
                 df: pd.DataFrame = None,
                 id_column: str = None,
                 review_column: str = None):
        """
        Take a data frame where each row is a comment/review

        :param df: a data frame where each row is a comment/review; The data frame should have at least an ID column
                   that stores the unique IDs of the comments, and a review column where the actual comments/reviews
                   are stored; default: None
        :param id_column: the name of the column that stores the unique IDs of the comments; default: None
        :param review_column: the name of the column where the actual comments/reviews are stored; default: None
        """
        if df is not None:

            self.df = df

            if id_column is not None:
                self._examine_id_column(df, id_column)
                self._id_column = id_column
            else:
                print("Haven't specified id_column (the name of the column that stores the unique IDs of the comments)")

            if review_column is not None:
                self._examine_review_column(df, id_column)
                self._review_column = review_column
            else:
                print("Haven't specified review_column (the name of the column where the actual comments/reviews are "
                      "stored)")

        else:
            print("There's no reviews data")

    @staticmethod
    def _examine_id_column(df, id_column):
        """
        Examine whether the column actually exists
        """
        if not isinstance(id_column, str):
            raise ColumnError("id_column should be a string")
        if id_column not in df.columns:
            raise ColumnError("id_column not in df.columns")

    @staticmethod
    def _examine_review_column(df, review_column):
        """
        Examine whether the column actually exists
        """
        if not isinstance(review_column, str):
            raise ColumnError("review_column should be a string")
        if review_column not in df.columns:
            raise ColumnError("review_column not in df.columns")

    @property
    def id_column(self):
        return self._id_column

    @property
    def review_column(self):
        return self._review_column

    @id_column.setter
    def id_column(self, new_id_column):
        self._examine_id_column(self.df, new_id_column)
        self._id_column = new_id_column

    @review_column.setter
    def review_column(self, new_review_column):
        self._examine_review_column(self.df, new_review_column)
        self._review_column = new_review_column
