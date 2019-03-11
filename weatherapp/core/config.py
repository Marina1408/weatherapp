# Application default verbose and log levels
DEFAULT_VERBOSE_LEVEL = 0
DEFAULT_MESSAGE_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'

# Fake user agentfor weather sites requests
FAKE_MOZILLA_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'

# Configuration settings
CONFIG_LOCATION = 'location'
CONFIG_FILE = 'weatherapp_ini'           # configuration file name

# Write to text file
WRITE_FILE = 'weatherapp.txt'

# Cache settings
CACHE_DIR = '.wappcache'       #cache directory name
CACH_TIME = 300                # how long cache files are valid(in seconds)

# entry points group for providers
PROVIDER_EP_NAMESPACE = 'weatherapp.provider'

