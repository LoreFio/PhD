# Data source:
# https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=f3c0f7d512273410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default

# Data meaning
# https://datos.madrid.es/FWProjects/egob/Catalogo/MedioAmbiente/Aire/Ficheros/Interprete_ficheros_%20calidad_%20del_%20aire_global.pdf

# Traffic data
# https://datos.madrid.es/sites/v/index.jsp?vgnextoid=33cb30c367e78410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD


madrid_data_dir = "data/Madrid"
zip_dir = "data/Madrid/Zip_folders"
pollutant_dict_madrid = {
    1: "SO2",
    6: "CO",
    7: "NO",
    8: "NO2",
    9: "PM25",
    10: "PM10",
    14: "O3",
}

station_prefix = "280790"

# Some stations changed the number during time => here we create a dict to unify the numbers using the convention
# old : new
station_code_dict = {
    "03": "35",
    "05": "39",
    "10": "38",
    "13": "40",
    "20": "36",
    "86": "60",
}


def convert_station_number(number_str):
    """Convert station numbers ensuring that the number is the new one

    :param number_str: number string
    :type number_str:  str
    :return: new number string
    :rtype: str
    """
    if not number_str.startswith(station_prefix):
        raise ValueError(f"{number_str} must start with prefix {station_prefix}")
    suffix = number_str[len(station_prefix):]
    if suffix in station_code_dict.keys():
        suffix = station_code_dict[suffix]
    return station_prefix + suffix

# Column variables


useless_col = ['PROVINCIA', 'MUNICIPIO', 'PUNTO_MUESTREO']
station_col = "ESTACION"
pollutant_col = 'MAGNITUD'
