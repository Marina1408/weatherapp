import os
import abc
import time
import urllib
import hashlib
import logging
import configparser
from pathlib import Path
from urllib.request import urlopen, Request

from weatherapp.core import config
from weatherapp.core.abstract.command import Command
from weatherapp.core.exception import RequestError, ConfigParserError


class WeatherProvider(Command):
	
	""" Weather provider abstract class.

	Defines behavior for all weather providers.
	"""

	logger = logging.getLogger(__name__)

	def __init__(self, app):

		super().__init__(app)

		location, url = self._get_configuration()
		self.location = location
		self.url = url

	@abc.abstractmethod
	def get_name(self):
		""" Provider name
		"""

	@abc.abstractmethod
	def get_default_location(self):
		""" Default location name.
		"""

	@abc.abstractmethod
	def get_default_url(self):
		""" Default location url.
		"""

	@abc.abstractmethod
	def configurate(self):
		""" Perfoms provider configuration.
		"""

	@abc.abstractmethod
	def get_weather_info(self, content):
		""" Collects weather information.

		Gets weather information from source and produce it in
		the following format.

		weather_info = {
		    'cond':         ''  # weather condition
		    'temp':         ''  # temperature
		    'feels_like':	''  # feels like temperature
		}
		"""

	@staticmethod
	def get_request_headers():
	    """Getting headers of the request.
	    """

	    return {'User-Agent': config.FAKE_MOZILLA_AGENT}

	@staticmethod
	def get_url_hash(url):
		""" Generate url hash.
		"""

		return hashlib.md5(url.encode('utf-8')).hexdigest()

	def save_cache(self, url, page_source):
	    """ Save page source data to file.
	    """

	    url_hash = self.get_url_hash(url)
	    cache_dir = self.get_cache_directory()
	    if not cache_dir.exists():
	    	cache_dir.mkdir(parents=True)

	    with (cache_dir / url_hash).open('wb') as cache_file:
	    	cache_file.write(page_source)

	@staticmethod
	def is_valid(path):
	    """ Check if cache is valid.
	    """

	    return (time.time() - path.stat().st_mtime) < config.CACH_TIME

	def get_cache(self, url):
	    """ Return cache by given url address if any.
	    """

	    cache = b''
	    url_hash = self.get_url_hash(url)
	    cache_dir = self.get_cache_directory()
	    if cache_dir.exists():
	    	cache_path = cache_dir / url_hash
	    	if cache_path.exists() and self.is_valid(cache_path):
	    		with cache_path.open('rb') as cache_file:
	    			cache = cache_file.read()

	    	return cache

	def get_page_source(self, url):
	    """ Getting page from server.
	    """

	    try:
	    	cache = self.get_cache(url)
	    	if cache and not self.app.options.refresh:
	    		page_source = cache
	    	else:
	    		request = Request(url, headers=self.get_request_headers())
	    		page_source = urlopen(request).read()
	    		self.save_cache(url, page_source)
	    	return page_source.decode('utf-8')
	    except (UnboundLocalError, urllib.error.HTTPError):
	    	self.clear_configurate()
	    	msg = 'Error!'
	    	if self.app.options.debug:
	    		self.logger.exception(msg)
	    	else:
	    		self.logger.error(msg)
	    	raise RequestError(self.app).run('Incorrectly set location!', 
	        	                             self.location)
	    
	def _get_configuration(self):
		""" Returns configurated location name and url
		"""

		name = self.get_default_location()
		url = self.get_default_url()
		parser = configparser.ConfigParser(interpolation=None)

		try:
			parser.read(self.get_configuration_file())
		except (configparser.Error, configparser.ParsingError,
			    configparser.MissingSectionHeaderError):
		    self.clear_configurate()
		    msg = 'Error!'
		    if self.app.options.debug:
		    	self.logger.exception(msg)
		    else:
		    	self.logger.error(msg)
		    raise ConfigParserError(self.app).run(('Bad configuration file. '
		    	          'Please reconfigurate your provider: '), self.name)		    	

		if self.get_name() in parser.sections():
			location_config = parser[self.get_name()]
			name, url = location_config['name'], location_config['url']

		return name, url

	def save_configuration(self, name, url):
	    """ Save selected location to configuration file.

	    We don't want to configure provider each time we use the
	    application, thus we save preferred location in configuration
	    file.

	    param name: cityname
	    param type: str

	    param url: preferred location URL
	    param type: str
	    """

	    parser = configparser.ConfigParser(interpolation=None)
	    config_file = self.get_configuration_file()

	    if config_file.exists():
	    	parser.read(config_file)

	    parser[self.get_name()] = {'name': name, 'url': url}
	    with open(config_file, 'w', 
	              encoding='utf-8') as configfile:
	        parser.write(configfile)

	def run(self, argv):
		""" Run provider.
		"""

		self.clear_not_valid_cache()

		content = self.get_page_source(self.url)
		return self.get_weather_info(content)

	def clear_not_valid_cache(self):
	    """ Clear all not valid cache.
	    """

	    cache_dir = self.get_cache_directory()
	    if cache_dir.exists():
	    	for file in os.listdir(cache_dir):
	    		if not self.is_valid(cache_dir/file):
	    			os.remove(cache_dir/file)
