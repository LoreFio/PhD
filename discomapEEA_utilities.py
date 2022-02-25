import re
import requests


def get_stat_data_name(url):
    """Extract station name from url

    :param url: API request url
    :type url: str
    :return: station_data code
    :rtype: str
    """
    tmp = re.sub(r"https\:\/\/ereporting\.blob\.core\.windows\.net\/downloadservice\/", "", url)
    tmp = re.sub(r"^[A-Z]{,2}\/", "", tmp)
    tmp = re.sub(r"^[A-Z]{,2}\_\d{1,}\_", "", tmp)
    return re.sub(r"\_timeseries\.csv", "", tmp)


def download_to_path(path, url):
    """Downloads API response into a file

    :param path: file path
    :type path: str
    :param url: API request url
    :type url: str
    """
    file = requests.get(url).content
    with open(path, 'wb') as output:
        output.write(file)


pollutant_dict_eea = {
    10: "CO",
    9: "NOX",
    8: "NO2",
    7: "O3",
    6001: "PM25",
    5: "PM10",
    1: "SO2"
}
URL_COL = "url"
EEA_data_dir = "data/discomapEEA"