import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from madrid_utilities import madrid_analysis_dir, madrid_all_file, datetime_col, pollutant_col, station_col

# https://stackoverflow.com/questions/29432629/plot-correlation-matrix-using-pandas


def save_corr_mat(df, discriminant_column, group_name):
    """Saves correlation matrix given a discriminant value

    :param df: input dataframe
    :type df: pd.DataFrame
    :param discriminant_column: column acting as discriminant
    :type discriminant_column: str
    :param group_name: name of the group of features
    :type group_name: str
    """
    discriminant_value = df[discriminant_column][0]
    df.drop([datetime_col, discriminant_column], axis=1, inplace=True)
    corr = df.corr()
    sns.heatmap(corr, annot=True, vmin=-1, vmax=1, cmap="YlOrRd")
    plt.title(f"Correlation matrix of {discriminant_column}_{discriminant_value}")
    plt.xlabel(group_name)
    plt.ylabel(group_name)
    plt.savefig(os.path.join(madrid_analysis_dir, f"{discriminant_column}_{discriminant_value}_corr.png"))


def save_stat(df, discriminant_column, group_name):
    """Saves correlation matrix given a discriminant value

    :param df: input dataframe
    :type df: pd.DataFrame
    :param discriminant_column: column acting as discriminant
    :type discriminant_column: str
    :param group_name: name of the group of features
    :type group_name: str
    """
    stat_dict = {"discriminant": discriminant_column,
                 "value": df[discriminant_column][0],
                 "first_day": df[datetime_col].min(),
                 "first_day": df[datetime_col].min(),
                 "missing": {col: df[col].isna().count() for col in df.columns}}


def smart_pivot(df, discriminant_column, pivot_column, value_column):
    """Transform input dataframe in n time series like dataframe where n is the number of unique items in
    discriminat_column

    :param df: input dataframe
    :type df: pd.DataFrame
    :param discriminant_column: column acting as discriminant
    :type discriminant_column: str
    :param pivot_column: column acting as pivot
    :type pivot_column: str
    :param value_column: column where values are contained
    :type value_column: str
    :return res: {disciminant: pd.DataFrame}
    :rtype res: dict
    """
    unique_discriminant = df[discriminant_column].unique()
    datetime_unique = df[datetime_col].unique()
    pivot_unique = df[pivot_column].unique()
    res = {}
    for disc in unique_discriminant:
        sub_df = df[df[discriminant_column] == disc]
        new_df = pd.DataFrame(datetime_unique, columns=[datetime_col])
        for pivot in pivot_unique:
            new_df = new_df.merge(sub_df[sub_df[pivot_column] == pivot][[value_column, datetime_col]],
                                  on=datetime_col, how="outer")
            new_df.columns = [el if el != value_column else str(pivot) for el in new_df.columns]
        new_df[discriminant_column] = disc
        res[disc] = new_df
    return res


if __name__ == "__main__":
    df = pd.read_pickle("ciao.pkl")
    res = smart_pivot(df=df, discriminant_column=station_col, pivot_column=pollutant_col,
                      value_column="concentration")
    save_corr_mat(df=list(res.values())[0], discriminant_column=station_col, group_name=pollutant_col)
    print(len(res))