# Data source:
# https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=f3c0f7d512273410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default

# Data meaning
# https://datos.madrid.es/FWProjects/egob/Catalogo/MedioAmbiente/Aire/Ficheros/Interprete_ficheros_%20calidad_%20del_%20aire_global.pdf

# Traffic data
# https://datos.madrid.es/sites/v/index.jsp?vgnextoid=33cb30c367e78410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD
import os

madrid_data_dir = "data/Madrid"
madrid_analysis_dir = "analysis/Madrid"
madrid_corr_dir = os.path.join(madrid_analysis_dir, "corr")
madrid_stat_dir = os.path.join(madrid_analysis_dir, "stat")
madrid_proc_dir = "data/Madrid_Processed"
zip_dir = "data/Madrid/Zip_folders"
madrid_all_file = os.path.join(madrid_proc_dir, "madrid_all_df.pkl")
pollutant_dict_madrid = {
    1: "SO2",
    6: "CO",
    7: "NO",
    8: "NO2",
    9: "PM25",
    10: "PM10",
    12: "NOx",
    14: "O3",
#    20: "TOL",
#    30: "BEN",
#    35: "EBE",
#    37: "MXY",
#    38: "PXY",
#    39: "OXY",
#    42: "TCH",
#    43: "CH4",
#    44: "NMHC",
}


def is_relevant_pollutant(x):
    """Returns whether x is a relevant pollutant

    :param x: pollutant code
    :type x: int
    :return: whether x is a relevant pollutant
    :rtype: bool
    """
    return x in pollutant_dict_madrid.keys()


station_prefix = "280790"
station_prefix_number = 100*int(station_prefix)

# Some stations changed the number during time => here we create a dict to unify the numbers using the convention
# old : new
station_code_dict = {
    3: 35,
    5: 39,
    10: 38,
    13: 40,
    20: 36,
    86: 60,
}


def convert_station_number(number):
    """Convert station numbers ensuring that the number is the new one

    :param number: number
    :type number: int
    :return: new number
    :rtype: int
    """
    if number in station_code_dict.keys():
        number = station_code_dict[number]
    return number

# Column variables


useless_col = ['PROVINCIA', 'MUNICIPIO', 'PUNTO_MUESTREO']
station_col = "station"
pollutant_col = 'pollutant'
station_col_old = "ESTACION"
pollutant_col_old = 'MAGNITUD'
date_columns = ['ANO', 'MES', 'DIA']
concentration_col = "concentration"
datetime_col = "datetime"