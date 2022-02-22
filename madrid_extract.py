import os
import pandas as pd
from madrid_utilities import madrid_data_dir, station_code_dict, convert_station_number, station_prefix, useless_col,\
    station_col, pollutant_col


def get_year_directories(data_dir):
    """Returns the list of all directories with yearly data

    :param data_dir: data directory
    :type data_dir: str
    :return: list of all directories with yearly data
    :rtype: list
    """
    return [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f)) and len(f) ==4]


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
    df_list = [open_clean_df(os.path.join(dir_path, file)) for file in file_list ]
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
    return data


def extract_station_from_year_df(data, station):
    """Extract a station data from yearly data

    :param data: year data
    :type data: pd.DataFrame
    :param station:
    :type station: str
    :return res_data: station data
    :rtype res_data: pd.DataFrame
    """
    station_data = data[data[station_col]==station]
    pollutant_list = list(station_data[pollutant_col].unique())
    res_data = pd.DataFrame(columns=["timedate", station_col] + pollutant_list)


    return res_data


def extract_all_ts():
    year_dirs = get_year_directories(madrid_data_dir)
    station_list = get_all_stations(madrid_data_dir)
    station_df_dict = {s: pd.DataFrame() for s in station_list}
    for year_dir in year_dirs:
        year_df = open_year_dir(dir_path=year_dir)
        for s in station_list:
            station_df_dict[s] = pd.concat([station_df_dict[s], extract_station_from_year_df(year_df)], axis=0)


if __name__ == "__main__":
    print(get_all_stations(madrid_data_dir))
