import os
import itertools
import numpy as np
import pandas as pd
from madrid_utilities import madrid_corr_dir, station_col, pollutant_col


def pair_to_str(pair):
    return pair[0] + "_" + pair[1]


def avg_corr(discriminant_column, corr_dir):
    """Computes average correlation for using a discriminant

    :param discriminant_column: column acting as discriminant
    :type discriminant_column: str
    :return mean_corr_df: DataFrame with correlation means
    :rtype mean_corr_df: pd.DataFrame
    """
    df_file_list = [file for file in os.listdir(corr_dir) if ".pkl" in file and discriminant_column in file]
    first_df = pd.read_pickle(os.path.join(corr_dir, df_file_list[0]))
    pivot_combinations = list(itertools.combinations(first_df.columns, 2))
    corr_dict = {pair_to_str(pair): {"count": 0, "mean": 0} for pair in pivot_combinations}
    for file in df_file_list:
        df = pd.read_pickle(os.path.join(corr_dir, file))
        for pair in pivot_combinations:
            value = df[pair[0]].loc[pair[1]]
            if not np.isnan(value):
                corr_dict[pair_to_str(pair)]["count"] += 1
                corr_dict[pair_to_str(pair)]["mean"] += value
    mean_corr_df = pd.DataFrame(corr_dict.keys(), columns=["pivot_combinations"])
    mean_corr_df["mean"] = [el["mean"] for el in corr_dict.values()]
    mean_corr_df["count"] = [el["count"] for el in corr_dict.values()]
    mean_corr_df["mean"] = mean_corr_df["mean"]/mean_corr_df["count"]
    mean_corr_df["abs_mean"] = mean_corr_df["mean"].apply(abs)
    mean_corr_df.sort_values("abs_mean", ascending=False, inplace=True)
    return mean_corr_df


if __name__ == "__main__":
    print(avg_corr(discriminant_column=station_col, corr_dir=madrid_corr_dir))
    print(avg_corr(discriminant_column=pollutant_col, corr_dir=madrid_corr_dir))
