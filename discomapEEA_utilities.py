import re
import io
import requests
import pandas as pd
from common_utilities import value_valid_mix


concentration_col = "Concentration"


def get_stat_data_name(url):
    """Extract station name from url

    :param url: API request url
    :type url: str
    :return: station_data code
    :rtype: str
    """
    tmp = re.sub(r"https\:\/\/ereporting\.blob\.core\.windows\.net\/downloadservice\/", "", url)
    tmp = re.sub(r"^[A-Z]{,2}\/", "", tmp)
    tmp = re.sub(r"^[A-Z]{,2}\_\d+\_", "", tmp)
    return re.sub(r"\_timeseries\.csv", "", tmp)


def eea_smart_download(path, url, to_filter):
    """Downloads API response into a file

    :param path: file path
    :type path: str
    :param url: API request url
    :type url: str
    :param to_filter: whether data need to be cleaned before
    :type to_filter: bool
    """
    file = requests.get(url).content
    io_str = io.StringIO(file.decode('utf-8'))
    if not to_filter:
        rawData = pd.read_csv(io_str, header=None, names=[url_col])
        return rawData
    else:
        # http://dd.eionet.europa.eu/vocabulary/aq/observationverification/view
        # http://dd.eionet.europa.eu/vocabulary/aq/observationvalidity/view
        rawData = pd.read_csv(io_str)
        rawData["Validity"] = (rawData["Validity"] == 1) & (rawData["Verification"] == 1)
        rawData[concentration_col] = rawData[[concentration_col, "Validity"]].apply(value_valid_mix)
        rawData.drop(['Namespace', 'AirQualityNetwork', 'AirQualityStationEoICode', 'SamplingPoint', 'SamplingProcess',
                      'Sample', 'AirPollutantCode', 'AveragingTime', 'UnitOfMeasurement', 'DatetimeEnd', 'Validity',
                      'Verification'], axis=1, inplace=True)
        rawData.to_pickle(path)
        return None


pollutant_dict_eea = {
    10: "CO",
    9: "NOX",
    8: "NO2",
    7: "O3",
    6001: "PM25",
    5: "PM10",
    1: "SO2"
}

url_col = "url"
eea_data_dir = "data/discomapEEA"
