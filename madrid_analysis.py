import os
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from madrid_utilities import madrid_corr_dir, madrid_stat_dir, madrid_all_file, madrid_analysis_dir, pollutant_col,\
    station_col, concentration_col, datetime_col

# https://matplotlib.org/stable/tutorials/colors/colormaps.html


def clean_analysis_dir():
    """Cleans the analysis directory from previously created files.

    """
    for file in os.listdir(madrid_stat_dir):
        os.remove(os.path.join(madrid_stat_dir, file))
    for file in os.listdir(madrid_corr_dir):
        os.remove(os.path.join(madrid_corr_dir, file))
    for file in os.listdir(madrid_analysis_dir):
        path = os.path.join(madrid_analysis_dir, file)
        if not os.path.isdir(path):
            os.remove(path=path)


def fill_missing_df(missing_dict):
    """Creates a dataframe resuming in a table information in missing_dict

    :param missing_dict: {discriminant: [missing_values]}
    :type missing_dict: dict
    :return missing_df: df showing which values are missing
    :rtype missing_df: pd.DataFrame
    """
    idx_values = set([el for value in missing_dict.values() for el in value])
    disc_list = list(missing_dict.keys())
    missing_df = pd.DataFrame(columns=disc_list, index=idx_values)
    for idx in idx_values:
        for disc in disc_list:
            missing_df[disc].loc[idx] = idx in missing_dict[disc]
    return missing_df


def find_missing_dates(df, discriminant_column):
    """Finds dates with only missing data of a dataframe

    :param df: input dataframe
    :type df: pd.DataFrame
    :param discriminant_column: column acting as discriminant
    :type discriminant_column: str
    :return: dates with all na
    :rtype: list
    """
    useful_cols = [col for col in df.columns if col not in [discriminant_column, datetime_col]]
    mask = df[useful_cols].isna().all(axis=1)
    return list(df[datetime_col][mask])


def find_missing_cols(df, discriminant_column):
    """Finds missing columns of a dataframe

    :param df: input dataframe
    :type df: pd.DataFrame
    :param discriminant_column: column acting as discriminant
    :type discriminant_column: str
    :return: columns with all na
    :rtype: list
    """
    length = len(df)
    return [col for col in df.columns
            if col not in [discriminant_column, datetime_col] and df[col].isna().sum() == length]


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
    df = df.drop([datetime_col, discriminant_column], axis=1, inplace=False)
    corr = df.corr()
    sns.heatmap(corr, annot=True, vmin=-1, vmax=1, cmap="YlOrRd")
    plt.title(f"Correlation matrix of {discriminant_column}_{discriminant_value}")
    plt.xlabel(group_name)
    plt.ylabel(group_name)
    plt.savefig(os.path.join(madrid_corr_dir, f"{discriminant_column}_{discriminant_value}_corr.png"))
    plt.close()
    corr.to_pickle(os.path.join(madrid_corr_dir, f"{discriminant_column}_{discriminant_value}_corr.pkl"))


def get_stat(df, discriminant_column):
    """Compute some statistics about the dataset

    :param df: input dataframe
    :type df: pd.DataFrame
    :param discriminant_column: column acting as discriminant
    :type discriminant_column: str
    :return: statistic dictionary
    :rtype: dict
    """
    return {"discriminant": discriminant_column,
            "value": df[discriminant_column][0],
            "first_date": df[datetime_col].min(),
            "last_date": df[datetime_col].max(),
            "length": len(df),
            "n_missing_row": df.shape[0]-df.dropna().shape[0],
            "missing_dict": {col: df[col].isna().sum() for col in df.columns if col != datetime_col}}


def save_stat(stat_dict):
    """Saves stat_dict from get_stat

    :param stat_dict: result of from get_stat
    :type stat_dict: dict
    """
    discriminant_column = stat_dict["discriminant"]
    discriminant_value = stat_dict["value"]
    with open(os.path.join(madrid_stat_dir, f"{discriminant_column}_{discriminant_value}_stat.pkl"), "wb") as f:
        pickle.dump(stat_dict, f)


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


def disc_analysis(df, discriminant_column, pivot_column, value_column):
    """Analyse input dataframe in n time series like dataframe where n is the number of unique items in
    discriminat_column

    :param df: input dataframe
    :type df: pd.DataFrame
    :param discriminant_column: column acting as discriminant
    :type discriminant_column: str
    :param pivot_column: column acting as pivot
    :type pivot_column: str
    :param value_column: column where values are contained
    :type value_column: str
    """
    disc_df = smart_pivot(df=df, discriminant_column=discriminant_column, pivot_column=pivot_column,
                          value_column=value_column)
    missing_cols_dict = {}
    missing_dates_dict = {}
    for el, df in tqdm(disc_df.items()):
        df.to_pickle(os.path.join(madrid_analysis_dir, f"{discriminant_column}_{el}_df.pkl"))
        stat_dict = get_stat(df, discriminant_column)
        print(stat_dict)
        save_stat(stat_dict=stat_dict)
        save_corr_mat(df=df, discriminant_column=discriminant_column, group_name=pivot_column)
        missing_cols_dict[el] = find_missing_cols(df=df, discriminant_column=discriminant_column)
        missing_dates_dict[el] = find_missing_dates(df=df, discriminant_column=discriminant_column)
    disc_missing_cols_df = fill_missing_df(missing_dict=missing_cols_dict)
    disc_missing_cols_df.to_pickle(os.path.join(madrid_analysis_dir, f"missing_df_{discriminant_column}.pkl"))


def full_analysis(file):
    """

    :param file:
    :return:
    """
    df = pd.read_pickle(file)
    disc_analysis(df, discriminant_column=station_col, pivot_column=pollutant_col, value_column=concentration_col)
    disc_analysis(df, discriminant_column=pollutant_col, pivot_column=station_col, value_column=concentration_col)


if __name__ == "__main__":
    clean_analysis_dir()
    file = madrid_all_file
    #  file = "ciao.pkl"
    full_analysis(file=file)
