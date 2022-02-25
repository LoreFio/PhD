import os


def clean_analysis_dir(analysis_dir):
    """Cleans the analysis directory from previously created files.

    """
    for el in os.listdir(analysis_dir):
        path = os.path.join(analysis_dir, el)
        if not os.path.isdir(path):
            os.remove(path=path)
        else:
            for subfile in os.listdir(path=path):
                os.remove(os.path.join(path, subfile))