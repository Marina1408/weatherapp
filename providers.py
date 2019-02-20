import time
import configparser
import hashlib
import re
import os
import html
import urllib.parse
from pathlib import Path
from urllib.request import urlopen, Request
from shutil import rmtree

from bs4 import BeautifulSoup

import config
import decorators


class WeatherProvider:
	""" Base weather provider.
	"""

	def __init__(self, app):
		self.app = app

		location, url = self.get_configuration()
		self.location = location
		self.url = url

	@staticmethod
	def get_request_headers():
	    """Getting headers of the request.
	    """

	    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}

	@staticmethod
	def get_url_hash(url):
	    return hashlib.md5(url.encode('utf-8')).hexdigest()

	@staticmethod
	def get_cache_directory():
	    """ Path to cach directory.
	    """

	    return Path.home() / config.CACHE_DIR

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
	    """ Check if current cache file is valid.
	    """

	    return (time.time() - path.stat().st_mtime) < config.CACH_TIME

	def get_cache(self, url):
	    """ Return cache data if any.
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

	@decorators.print_args
	def get_page_source(self, url):
	    """ Getting page from server.
	    """

	    cache = self.get_cache(url)
	    if cache and not self.app.options.refresh:
	    	page_source = cache
	    else:
	    	request = Request(url, headers=self.get_request_headers())
	    	page_source = urlopen(request).read()
	    	self.save_cache(url, page_source)

	    return page_source.decode('utf-8')

	def get_configuration(self):
		""" Returns configurated location name and url
		"""

		name = self.default_location
		url = self.default_url
		parser = configparser.ConfigParser(interpolation=None)
		parser.read(self.get_configuration_file())

		if config.CONFIG_LOCATION in parser.sections():
			location_config = parser[config.CONFIG_LOCATION]
			name, url = location_config['name'], location_config['url']

		return name, url

	def save_configuration(self, name, url):
	    """ Save selected location to configuration file.
	    """

	    parser = configparser.ConfigParser(interpolation=None)
	    parser[config.CONFIG_LOCATION] = {'name': name, 'url': url}
	    with open(self.get_configuration_file(), 'w', 
	              encoding='utf-8') as configfile:
	        parser.write(configfile)

	def clear_configurate(self):
	    """ Clear configurate file for weather site.
	    """

	    os.remove(self.get_configuration_file())

	@decorators.one_moment
	def run(self):
		""" Run provider.
		"""

		self.clear_not_valid_cache()

		content = self.get_page_source(self.url)
		return self.get_weather_info(content)

	def clear_all_cache(self):
	    """ Clear all cache files and the cache directory.
	    """

	    cache_dir = self.get_cache_directory()
	    rmtree(cache_dir)

	@decorators.slow_down(sec=5)
	def clear_not_valid_cache(self):
	    """ Clear all not valid cache.
	    """

	    cache_dir = self.get_cache_directory()
	    if cache_dir.exists():
	    	for file in os.listdir(cache_dir):
	    		if not self.is_valid(cache_dir/file):
	    			os.remove(cache_dir/file)


class AccuWeatherProvider(WeatherProvider):

	""" Weather provider for AccuWeather site.
	"""

	name = config.ACCU_PROVIDER_NAME
	title = config.ACCU_PROVIDER_TITLE

	default_location = config.DEFAULT_ACCU_LOCATION_NAME
	default_url = config.DEFAULT_ACCU_LOCATION_URL

	@staticmethod
	def get_configuration_file():
	    """ Path to configuration file.
	    """

	    return Path.home() / config.CONFIG_FOLDER / config.CONFIG_FILE_ACCU

	def get_locations_accu(self, locations_url):
	    """ Getting locations from accuweather.
	    """

	    locations_page = self.get_page_source(locations_url)
	    soup = BeautifulSoup(locations_page, 'html.parser')

	    locations = []
	    for location in soup.find_all('li', class_='drilldown cl'):
	    	url = location.find('a').attrs['href']
	    	location = location.find('em').text
	    	locations.append((location, url))
	    return locations

	def configurate_accu(self, r_defaults=False):
	    """ Displays the list of locations for the user to select from 
	        AccuWeather.
	    """

	    if not r_defaults:
	    	locations = self.get_locations_accu(config.ACCU_BROWSE_LOCATIONS)
	    	while locations:
	    		for index, location in enumerate(locations):
	    			print(f'{index + 1}. {location[0]}')
	    		selected_index = int(input('Please select location: '))
	    		location = locations[selected_index - 1]
	    		locations = self.get_locations_accu(location[1])
	    	self.save_configuration(*location)
	    else:
	    	self.clear_configurate()

	def get_weather_info(self, page_content):
	    """ Getting the final result in tuple from site accuweather.
	    """

	    city_page = BeautifulSoup(page_content, 'html.parser')
	    weather_info = {}
	    if not self.app.options.tomorrow:
	    	current_day_selection = city_page.find\
	    	         ('li', class_=re.compile('(day|night) current first cl'))
	    	if current_day_selection:
	    		current_day_url = \
	    		                current_day_selection.find('a').attrs['href']
	    		if current_day_url:
	    			current_day_page = self.get_page_source(current_day_url)
	    			if current_day_page:
	    				current_day = BeautifulSoup(current_day_page,
                                                    'html.parser')
	    				weather_details = current_day.find('div',
                                                   attrs={'id': 'detail-now'})
	    				condition = weather_details.find('span', 
	    					                             class_='cond')
	    				if condition:
	    					weather_info['cond'] = condition.text
	    				temp = weather_details.find('span', 
	    					                         class_='large-temp')
	    				if temp:
	    					weather_info['temp'] = temp.text
	    				feal_temp = weather_details.find(
                            'span', class_='small-temp')
	    				if feal_temp:
	    					weather_info['feal_temp'] = feal_temp.text
	    else:
	    	tomorrow_day_selection = city_page.find('li',
                                                    class_='day last hv cl')
	    	if tomorrow_day_selection:
	    		tomorrow_day_url = \
	    		                tomorrow_day_selection.find('a').attrs['href']
	    		if tomorrow_day_url:
	    			tomorrow_day_page = self.get_page_source(tomorrow_day_url)
	    			if tomorrow_day_page:
	    				tomorrow_day = BeautifulSoup(tomorrow_day_page,
                                                     'html.parser')
	    				weather_details = tomorrow_day.find('div',
                                             attrs={'id': 'detail-day-night'})
	    				condition = weather_details.find('div', class_='cond')
	    				if condition:
	    					weather_info['cond'] = condition.text.strip()
	    				temp = weather_details.find('span', 
	    					                         class_='large-temp')
	    				if temp:
	    					weather_info['temp'] = temp.text
	    				feal_temp = weather_details.find('span', 
                                                         class_='realfeel')
	    				if feal_temp:
	    					weather_info['feal_temp'] = feal_temp.text

	    return weather_info


class Rp5WeatherProvider(WeatherProvider):

	""" Weather provider for RP5 site.
	"""

	name = config.RP5_PROVIDER_NAME
	title = config.RP5_PROVIDER_TITLE

	default_location = config.DEFAULT_RP5_LOCATION_NAME
	default_url = config.DEFAULT_RP5_LOCATION_URL

	@staticmethod
	def get_configuration_file():
	    """ Path to configuration file.\
	    """

	    return Path.home() / config.CONFIG_FOLDER / config.CONFIG_FILE_RP5

	def get_locations_rp5(self, locations_url):
	    """ Getting locations from rp5.ua.
	    """

	    locations_page = self.get_page_source(locations_url)
	    soup = BeautifulSoup(locations_page, 'html.parser')
	    part_url = ''

	    locations = []
	    for location in soup.find_all('div', class_='country_map_links'):
	    	part_url = location.find('a').attrs['href']
	    	part_url = urllib.parse.quote(part_url)
	    	url = config.base_url_rp5 + part_url
	    	location = location.find('a').text
	    	locations.append((location, url))
	    if locations == []:
	    	for location in soup.find_all('h3'):
	    		part_url = location.find('a').attrs['href']
	    		part_url = urllib.parse.quote(part_url)
	    		url = config.base_url_rp5 + '/' + part_url
	    		location = location.find('a').text
	    		locations.append((location, url))

	    return locations

	def configurate_rp5(self, r_defaults=False):
	    """ Displays the list of locations for the user to select from RP5.
	    """

	    if not r_defaults:
	    	locations = self.get_locations_rp5(config.RP5_BROWSE_LOCATIONS)
	    	while locations:
	    		for index, location in enumerate(locations):
	    			print(f'{index + 1}. {location[0]}')
	    		selected_index = int(input('Please select location: '))
	    		location = locations[selected_index - 1]
	    		locations = self.get_locations_rp5(location[1])

	    	self.save_configuration(*location)
	    else:
	    	self.clear_configurate()

	@decorators.timer
	def get_weather_info(self, page_content):
	    """ Getting the final result in tuple from site rp5.
	    """

	    city_page = BeautifulSoup(page_content, 'html.parser')
	    weather_info = {}
	    if not self.app.options.tomorrow:
	    	weather_details = city_page.find('div', 
	    		                      attrs={'id': 'archiveString'})
	    	weather_details_cond = weather_details.find('div', 
	    		                                   class_='ArchiveInfo')
	    	conditions = weather_details.get_text()
	    	condition = str(conditions[conditions.find('F,')+3:])
	    	if condition:
	    		weather_info['cond'] = condition
	    	weather_details_temp = weather_details.find('div',
                                                    class_='ArchiveTemp')
	    	temp = weather_details_temp.find('span', class_='t_0')
	    	if temp:
	    		weather_info['temp'] = temp.text
	    	weather_details_feal_temp = weather_details.find('div',
                                                class_='ArchiveTempFeeling')
	    	feal_temp = weather_details_feal_temp.find('span', class_='t_0')
	    	if feal_temp:
	    		weather_info['feal_temp'] = feal_temp.text
	    else:
	    	weather_details = city_page.find('div', attrs={'id': 
                                                   'forecastShort-content'})
	    	weather_details_tomorrow = weather_details.find('span',
                                                        class_='second-part')
	    	conditions = weather_details_tomorrow.findPrevious('b').text
	    	condition_all = str(conditions[conditions.find('Завтра:')+28:])
	    	condition = str(condition_all[condition_all.find('F,')+3:])
	    	if condition:
	    		weather_info['cond'] = condition
	    	temp = weather_details_tomorrow.find('span', class_='t_0')
	    	if temp:
	    		weather_info['temp'] = temp.text

	    return weather_info


class SinoptikWeatherProvider(WeatherProvider):

	""" Weather provider for Sinoptik.ua site.
	"""

	name = config.SINOPTIK_PROVIDER_NAME
	title = config.SINOPTIK_PROVIDER_TITLE

	default_location = config.DEFAULT_SINOPTIK_LOCATION_NAME
	default_url = config.DEFAULT_SINOPTIK_LOCATION_URL

	@staticmethod
	def get_configuration_file():
	    """ Path to configuration file.
	    """

	    return (Path.home() / config.CONFIG_FOLDER /
	                          config.CONFIG_FILE_SINOPTIK)

	def configurate_sinoptik(self, r_defaults=False):
	    """ Asking the user to input the city.
	    """

	    if not r_defaults:
		    base_url = 'https://ua.sinoptik.ua'
		    part_1_url = '/погода-'
		    part_1_url = urllib.parse.quote(part_1_url)
		    location = input('Введіть назву міста: \n')
		    part_2_url = urllib.parse.quote(location)
		    url = base_url + part_1_url + part_2_url
		    self.save_configuration(location, url)
	    else:
		    self.clear_configurate()

	@decorators.timer
	def get_weather_info(self, page_content):
	    """ Getting the final result in tuple from sinoptik.ua site.
	    """

	    city_page = BeautifulSoup(page_content, 'html.parser')
	    weather_info = {}
	    weather_details = city_page.find('div', class_='tabsContent')
	    if not self.app.options.tomorrow:
	    	weather_details = city_page.find('div', class_='tabsContent')
	    	condition_weather_details = weather_details.find('div', 
                                      class_='wDescription clearfix')
	    	condition = condition_weather_details.find('div', 
                                                class_='description')
	    	if condition:
	    		weather_info['cond'] = condition.text.strip()
	    	temp = weather_details.find('p', class_='today-temp')
	    	if temp:
	    		weather_info['temp'] = temp.text
	    	weather_details_feal_temp = weather_details.find('tr',
                                        class_='temperatureSens')
	    	feal_temp = weather_details_feal_temp.find('td', 
	    		          class_=re.compile(
                          '(p5 cur)|(p1)|(p2 bR)|(p3)|(p4 bR)|(p5)|(p6 bR)|'
                          '(p7 cur)|(p8)'))
	    	if feal_temp:
	    		weather_info['feal_temp'] = feal_temp.text
	    else:
	    	weather_details = city_page.find('div', attrs={'id': 'bd2'})
	    	temp = weather_details.find('div', class_='max')
	    	if temp:
	    		weather_info['temp'] = temp.text
	    	feal_temp = weather_details.find('div', class_='min')
	    	if feal_temp:
	    		weather_info['feal_temp'] = feal_temp.text
	    	tomorrow_day_selection = city_page.find('div',
                                             attrs={'id': 'bd2'})
	    	if tomorrow_day_selection:
	    		part_url = tomorrow_day_selection.find('a').attrs['href']
	    		part_url = urllib.parse.quote(part_url)
	    		base_url = 'http:' 
	    		tomorrow_day_url = base_url + part_url
	    		if tomorrow_day_url:
	    			tomorrow_day_page = self.get_page_source(tomorrow_day_url)
	    			if tomorrow_day_page:
	    				tomorrow_day = BeautifulSoup(tomorrow_day_page,
                                                 'html.parser')
	    				weather_details = tomorrow_day.find('div',
                                             class_='wDescription clearfix')
	    				condition = weather_details.find('div', 
                                                     class_='description')
	    				if condition:
	    					weather_info['cond'] = condition.text.strip()

	    return weather_info

	






























