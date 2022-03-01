import os
import pandas as pd
from tqdm import tqdm
from datetime import datetime

from common_utilities import value_valid_mix
from madrid_utilities import madrid_data_dir, convert_station_number, useless_col, station_col_old, date_columns, \
    madrid_all_file, pollutant_col_old, pollutant_dict_madrid, concentration_col, datetime_col, pollutant_col,\
    station_col, is_relevant_pollutant

valid_col = "valid"
hour_col = "hour"


def get_year_directories(data_dir):
    """Returns the list of all directories with yearly data

    :param data_dir: data directory
    :type data_dir: str
    :return: list of all directories with yearly data
    :rtype: list
    """
    return [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f)) and len(f) == 4]


def get_all_stations(data_dir):
    """Returns the list of all measurement stations

    :param data_dir: data directory
    :type data_dir: str
    :return: list of all stations
    :rtype: list
    """
    list_dir = sorted(get_year_directories(data_dir=data_dir))
    most_recent_dir = os.path.join(data_dir, list_dir[-1])
    most_recent_file = os.listdir(most_recent_dir)[0]
    data = open_clean_df(filename=os.path.join(most_recent_dir, most_recent_file))
    data[station_col] = data[station_col].apply(convert_station_number)
    return list(data[station_col].unique())


def open_year_dir(dir_path):
    """Opens, cleans and joins all dataframe of one directory.

    :param dir_path: directory path
    :type dir_path: str
    :return: yearly data
    :rtype: pd.DataFrame
    """
    file_list = os.listdir(dir_path)
    df_list = [open_clean_df(os.path.join(dir_path, file)) for file in file_list]
    return pd.concat(df_list, axis=0)


def open_clean_df(filename):
    """Extract data from a file

    :param filename: filename
    :type filename: str
    :return data: year data
    :rtype data: pd.DataFrame
    """
    data = pd.read_csv(filename, sep=";")
    data.drop(useless_col, axis=1, inplace=True)
    data.columns = [x if x != pollutant_col_old else pollutant_col for x in data.columns]
    data.columns = [x if x != station_col_old else station_col for x in data.columns]
    data = data[data[pollutant_col].apply(is_relevant_pollutant)]
    return data


def cols2datetime(x):
    """Convert multiple columns to datetime format

    :param x: iterable containing year, month, day and a string idetifying the hour of the day
    :type x: iterable
    :return: datetime
    :rtype: datetime.datetime
    """
    return datetime(year=x[0], month=x[1], day=x[2], hour=int(x[3][1:])-1)


def convert_from_year_df(data):
    """Extract a station data from yearly data

    :param data: year data
    :type data: pd.DataFrame
    :return res_data: station data
    :rtype res_data: pd.DataFrame
    """
    hours_cols = [col for col in data.columns if col.startswith("H")]
    valid_cols = [col for col in data.columns if col.startswith("V")]
    useful_cols = [col for col in data.columns if col not in hours_cols+valid_cols]
    melted_hour_df = pd.melt(data, id_vars=useful_cols, value_vars=hours_cols, var_name=hour_col,
                             value_name=concentration_col)
    melted_valid_df = pd.melt(data, id_vars=[], value_vars=valid_cols, var_name=hour_col,
                              value_name=valid_col)
    melted_hour_df[valid_col] = melted_valid_df[valid_col].apply(lambda x: x == "V")
    melted_hour_df[datetime_col] = melted_hour_df[date_columns + [hour_col]].apply(cols2datetime, axis=1)
    melted_hour_df[concentration_col] = melted_hour_df[[concentration_col, valid_col]].apply(value_valid_mix, axis=1)
    melted_hour_df.drop(date_columns + [hour_col, valid_col], axis=1, inplace=True)
    return melted_hour_df


def extract_all_ts(data_dir):
    """Returns the list of all measurement stations

    :param data_dir: data directory
    :type data_dir: str
    :return: list of all stations
    :rtype: list
    """
    year_dirs = get_year_directories(data_dir)
    all_df = pd.concat([convert_from_year_df(open_year_dir(dir_path=os.path.join(data_dir, year_dir)))
                        for year_dir in tqdm(year_dirs)], axis=0)
    all_df.reset_index(inplace=True, drop=True)
    all_df[station_col] = all_df[station_col].apply(int)
    all_df[pollutant_col] = all_df[pollutant_col].apply(int)
    all_df[pollutant_col] = all_df[pollutant_col].apply(lambda x: pollutant_dict_madrid[x])
    return all_df


if __name__ == "__main__":
    all_df = extract_all_ts(data_dir=madrid_data_dir)
    all_df.to_pickle(madrid_all_file)
