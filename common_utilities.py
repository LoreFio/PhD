import os
import shutil

import numpy as np


def clean_download_dir(download_dir):
    """Cleans the download directory from previously created files. Removes subdirs as well

    :param download_dir: download directory
    :type download_dir: str
    """
    shutil.rmtree(download_dir)


def clean_analysis_dir(analysis_dir):
    """Cleans the analysis directory from previously created files.

    :param analysis_dir: analysis directory
    :type analysis_dir: str
    """
    for el in os.listdir(analysis_dir):
        path = os.path.join(analysis_dir, el)
        if not os.path.isdir(path):
            os.remove(path=path)
        else:
            for subfile in os.listdir(path=path):
                os.remove(os.path.join(path, subfile))


def value_valid_mix(x):
    """Convert value to np.nan if value is not valid

    :param x: iterable containing value and validity boolean
    :type x: iterable
    :return: value or np.nan
    :rtype: float
    """
    if x[1]:
        return x[0]
    else:
        return np.nan