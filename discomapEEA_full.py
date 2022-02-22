import os
import re
import requests
import pandas as pd
from tqdm import tqdm

# For more details
# https://discomap.eea.europa.eu/map/fme/AirQualityExport.htm

data_dir = "data/discomapEEA"
URL_COL = "url"
pollutant_dict_eea = {
    10: "CO",
    9: "NOX",
    8: "NO2",
    7: "O3",
    6001: "PM25",
    5: "PM10",
    1: "SO2"
}


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


if __name__ == "__main__":

    CountryCode = 'BE'
    CityName = "Bruxelles / Brussel"  # [Antwerpen, Brugge, Bruxelles / Brussel, ...]
    Year_from = 2017  #
    Year_to = 2021

    for p_number, p_name in pollutant_dict_eea.items():
        print(f"Looking for {p_name} data")

        first_url = f"https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw?CountryCode={CountryCode}&CityName={CityName}&Pollutant={p_number}&Year_from={Year_from}&Year_to={Year_to}&Station=&Samplingpoint=&Source=All&Output=TEXT&UpdateDate=&TimeCoverage=Year"
        first_url = first_url.replace(" ", "%20")

        tmp_file = os.path.join(data_dir, "tmp.csv")
        download_to_path(path=tmp_file, url=first_url)
        print("Hub file downloaded")
        sub_url_data = pd.read_csv(tmp_file, header=None, names=[URL_COL])

        if len(sub_url_data) > 0:
            output_dir = os.path.join(data_dir, f"{CountryCode}_{CityName[:3]}_{Year_from}_{Year_to}_{p_name}")
            os.mkdir(output_dir)
            for url in tqdm(sub_url_data[URL_COL]):
                station_name = get_stat_data_name(url=url)
                file_name = station_name + ".csv"
                download_to_path(os.path.join(output_dir, file_name), url=url)
            print(f"Download completed for {p_name}")
        else:
            print(f"no pollutant data found for {p_name}")
        os.remove(tmp_file)
