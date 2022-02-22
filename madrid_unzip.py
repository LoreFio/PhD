import os
import re
import zipfile
from tqdm import tqdm
from madrid_utilities import madrid_data_dir, zip_dir


def get_year(file_name):
    """Extract year from

    :param file_name: file name
    :type file_name: str
    :return: year of the data
    :rtype: str
    """
    tmp = re.sub(r"Anio", "", file_name)
    tmp = re.sub(r"\.\w+", "", tmp)
    return tmp[:4]


if __name__ == "__main__":
    dir_content = os.listdir(zip_dir)
    for content in tqdm(dir_content):
        file_path = os.path.join(zip_dir, content)
        year_str = get_year(content)
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path) as zf:
                for member in zf.infolist():
                    if "csv" in member.filename:
                        zf.extract(member=member, path=os.path.join(madrid_data_dir, year_str))
