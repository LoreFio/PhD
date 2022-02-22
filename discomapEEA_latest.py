# Python sample for download of air quality up-to-date files
# The Pyton script shows a simple sample how the pre-processed CSV files can be downloaded.
# EEA takes no responsibility of the script and the code is provided 'as is', without warranty of any kind.
# Peter Kjeld, 15. February 2019

import requests

print('-----------------------------------------------------------------------')

# Set download url
ServiceUrl = "http://discomap.eea.europa.eu/map/fme/latest"

# Countries to download
# Note: List is not complete
countries = ['BE', 'IT']

# Pollutant to be downloaded
pollutants = ['C6H6', 'PM10', 'CO', 'NO2', 'SO2', 'O3', 'PM2.5']

for country in countries:
    for pollutant in pollutants:
        fileName = "data/discomapEEA/%s_%s.csv" % (country, pollutant)
        downloadFile = '%s/%s_%s.csv' % (ServiceUrl, country, pollutant)
        # Download and save to local path
        print('Downloading: %s' % downloadFile)
        file = requests.get(downloadFile).content
        with open(fileName, 'wb') as output:
            output.write(file)
        print('Saved locally as: %s ' % fileName)
        print('-----')
    print('Download finished')


