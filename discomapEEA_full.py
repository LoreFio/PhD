import os
import pandas as pd
from tqdm import tqdm
from common_utilities import clean_download_dir
from discomapEEA_utilities import get_stat_data_name, pollutant_dict_eea, url_col, eea_data_dir, eea_smart_download
# For more details
# https://discomap.eea.europa.eu/map/fme/AirQualityExport.htm


def download_eea(country_code, city_name, year_from, year_to):
    for p_number, p_name in pollutant_dict_eea.items():
        print(f"Looking for {p_name} data")

        first_url = f"https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw?" \
                    f"CountryCode={country_code}&CityName={city_name}&Pollutant={p_number}&Year_from={year_from}&" \
                    f"Year_to={year_to}&Station=&Samplingpoint=&Source=All&Output=TEXT&UpdateDate=&TimeCoverage=Year"
        first_url = first_url.replace(" ", "%20")

        tmp_file = eea_smart_download(path=tmp_file, url=first_url, to_filter=False)
        print("Hub file downloaded")
        sub_url_data = pd.read_csv(tmp_file, header=None, names=[url_col])

        if len(sub_url_data) > 0:
            output_dir = os.path.join(eea_data_dir, f"{country_code}_{city_name[:3]}_{year_from}_{year_to}_{p_name}")
            os.mkdir(output_dir)
            for url in tqdm(sub_url_data[url_col]):
                station_name = get_stat_data_name(url=url)
                file_name = station_name + ".pkl"
                eea_smart_download(os.path.join(output_dir, file_name), url=url)
            print(f"Download completed for {p_name}")
        else:
            print(f"no pollutant data found for {p_name}")


if __name__ == "__main__":
    clean_download_dir(eea_data_dir)
    country_code = 'BE'
    city_name = "Bruxelles / Brussel"  # [Antwerpen, Brugge, Bruxelles / Brussel, ...]
    year_from = 2013  #
    year_to = 2021
    download_eea(country_code=country_code, city_name=city_name, year_from=year_from, year_to=year_to)