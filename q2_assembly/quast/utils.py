import pandas as pd

from q2_assembly.quast.report import MANDATORY_COLS_MAP, OPTIONAL_COLS_MAP
from q2_assembly.quast.types import QUASTResultsFormat


def _parse_columns(report_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function will rename and select the needed columns of the QUAST
    results.

    Args:
        - report_df(pd.Dataframe): Dataframe containing the QUAST results

    Returns:
        a Pandas dataframe with the renamed columns.
    """
    report_df_newcols = report_df.copy()
    report_df_newcols.rename(columns=MANDATORY_COLS_MAP, inplace=True)
    optional_cols = []

    # find the optional columns
    optional_columns_present = set(OPTIONAL_COLS_MAP.keys()).intersection(
        report_df_newcols.columns
    )
    for col in optional_columns_present:
        report_df_newcols.rename(columns={col: OPTIONAL_COLS_MAP[col]}, inplace=True)
        optional_cols.append(OPTIONAL_COLS_MAP[col])

    # make sure that in the final table we have the values we
    # specify in the dicts in a certain order
    all_cols = QUASTResultsFormat.HEADER + optional_cols
    report_df_newcols = report_df_newcols[all_cols]
    report_df_newcols["id"] = report_df_newcols["id"].str.replace("_contigs", "")

    report_df_newcols = report_df_newcols.set_index("id")

    return report_df_newcols