import numpy as np
import pandas as pd
from beartype import beartype
from beartype.typing import Sequence

from eis_toolkit.exceptions import InvalidColumnIndexException, InvalidCompositionException
from eis_toolkit.utilities.checks.coda import check_compositional
from eis_toolkit.utilities.checks.dataframe import check_column_index_in_dataframe


@beartype
def _alr_transform_old(df: pd.DataFrame, columns: Sequence[str], denominator_column: str) -> pd.DataFrame:

    ratios = df[columns].div(df[denominator_column], axis=0)
    return np.log(ratios)


@beartype
def _alr_transform(df: pd.DataFrame, columns: Sequence[str], denominator_column: str) -> pd.DataFrame:

    ratios = df[columns].div(df[denominator_column], axis=0)
    return np.log(ratios)


@beartype
@check_compositional
def alr_transform(df: pd.DataFrame, idx: int = -1, keep_redundant_column: bool = False) -> pd.DataFrame:
    """
    Perform an additive logratio transformation on the data.

    Args:
        df: A dataframe of compositional data.
        idx: The integer position based index of the column of the dataframe to be used as denominator.
            If not provided, the last column will be used.
        keep_redundant_column: Whether to include the denominator column in the result. If True, it is
            included in the output dataframe regardless of whether it was in the list of given input columns.

    Returns:
        A new dataframe containing the ALR transformed data.

    Raises:
        InvalidColumnException: One or more input columns are not found in the given dataframe, or the
            numerator or denominator columns contain zeros.
        InvalidColumnIndexException: The input index for the denominator column is out of bounds.
        InvalidParameterValueException: Too few columns to perform the transformation.
    """
    if df.isnull().values.any():
        raise InvalidCompositionException("Data contains NaN values.")

    columns = [col for col in df.columns]

    if not check_column_index_in_dataframe(df, idx):
        raise InvalidColumnIndexException("Denominator column index out of bounds.")

    denominator_column = df.columns[idx]

    # TODO: decide: should redundant column maintain its relative
    # position to the other columns in the resulting dataframe?
    if denominator_column not in columns:
        columns.append(denominator_column)

    if not keep_redundant_column and denominator_column in columns:
        columns.remove(denominator_column)

    return _alr_transform(df, columns, denominator_column)


def inverse_alr():
    """Perform the inverse transformation for a set of ALR transformed data."""
    raise NotImplementedError()