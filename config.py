# Configuration settings
CONFIG_LOCATION = 'location'
CONFIG_FOLDER = 'weatherapp_ini'           # configuration directory name
CONFIG_FILE_ACCU = 'accu_weatherapp.ini'     
CONFIG_FILE_RP5 = 'rp5_weatherapp.ini'
CONFIG_FILE_SINOPTIK = 'sinoptik_weatherapp.ini'

# Write to text file
WRITE_FILE = 'weatherapp.txt'

# Cache settings
CACHE_DIR = '.wappcache'       #cache directory name
CACH_TIME = 300                # how long cache files are valid(in seconds)

# AccuWeather provider related configuration
ACCU_PROVIDER_NAME = 'accu'             # provider ID
ACCU_PROVIDER_TITLE = 'AccuWeather'     # provider title

DEFAULT_ACCU_LOCATION_NAME = 'Kyiv'
DEFAULT_ACCU_LOCATION_URL = ('https://www.accuweather.com/uk/ua/kyiv/324505/'
                    'weather-forecast/324505')
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'

# RPA.ua provider related configuration
RP5_PROVIDER_NAME = 'rp5'               # provider ID
RP5_PROVIDER_TITLE = 'RP5.ua'           # provider title

DEFAULT_RP5_LOCATION_NAME = 'Kyiv'
DEFAULT_RP5_LOCATION_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D'
	                        '0%B0_%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96')
RP5_BROWSE_LOCATIONS = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0'
                        '%B0_%D0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96')
base_url_rp5 = 'http://rp5.ua'

# Sinoptik.ua provider related configuration
SINOPTIK_PROVIDER_NAME = 'sinoptik'        # provider ID
SINOPTIK_PROVIDER_TITLE = 'SINOPTIK.UA'    # provider title

DEFAULT_SINOPTIK_LOCATION_NAME = 'Kyiv'
DEFAULT_SINOPTIK_LOCATION_URL = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%'
	                         'B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D1%97%D0%B2')
SINOPTIK_BROWSE_LOCATIONS = 'https://ua.sinoptik.ua/'




