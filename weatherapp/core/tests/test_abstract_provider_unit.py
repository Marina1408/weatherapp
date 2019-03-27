import os
import time
import hashlib
import urllib
import unittest
import configparser
from pathlib import Path
from shutil import rmtree
from urllib.request import urlopen, Request


from weatherapp.core.abstract import WeatherProvider


class ProviderAbstractTestCase(unittest.TestCase):

	""" Unit test case for abstract provider.
	"""

	def setUp(self):
		self.url =  ('https://www.accuweather.com/uk/ua/kyiv/324505/'
                     'weather-forecast/324505')
		self.name = 'Kyiv'
		self.cache = 'cache'
		self.cache_path = Path.home() / self.cache
		self.headers = WeatherProvider.get_request_headers()

	def test_get_request_headers(self):
		""" Test 'get_request_headers' method.
		"""

		self.assertEqual(self.headers, 
			{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'})

	def test_get_url_hash(self):
		""" Test 'get_url_hash' method.
		"""

		url_hash = WeatherProvider.get_url_hash(self.url)
		self.assertTrue(url_hash)
		self.assertEqual(url_hash, '6542d16ae49fd8c20e2b9b4f9fa195ff')

	def test_save_get_cache(self):
		""" Test 'save_cache' and 'get_cache' methods.
		"""

		url_hash = WeatherProvider.get_url_hash(self.url)

		page_source = b'1'

		if not self.cache_path.exists():
			self.cache_path.mkdir(parents=True)

		with (self.cache_path / url_hash).open('wb') as cache_file:
			cache_file.write(page_source)

		self.assertTrue(url_hash)
		self.assertTrue(page_source)
		self.assertEqual(page_source, b'1')

		if (self.cache_path / url_hash).exists():
			with (self.cache_path / url_hash).open('rb') as cache_file:
				cache = cache_file.read()

		self.assertTrue(url_hash)
		self.assertTrue(page_source)
		self.assertEqual(page_source, b'1')

		rmtree(self.cache_path)

	def test_is_valid(self):
		""" Test 'is_valid' method.
		""" 

		if not self.cache_path.exists():
			self.cache_path.mkdir(parents=True)

		timer = time.time() - self.cache_path.stat().st_mtime
		cache_time = 100

		self.assertLess(timer, cache_time)

	def test_get_page_source(self):
		""" Test 'get_page_source' method.
		"""

		request = Request(self.url, headers=self.headers)
		page_source = urlopen(request).read()
		page_source_dec = page_source.decode('utf-8')

		self.assertTrue(request)
		self.assertTrue(page_source_dec)

	def test__save_get_configuration(self):
		""" Test '_get_configuration' and 'save_configuration' methods.
		"""

		parser = configparser.ConfigParser(interpolation=None)

		config_file = 'config_file'
		config_path = Path.home() / config_file

		parser['dummy'] = {'name': self.name, 'url': self.url}
		with open(config_path, 'w', encoding='utf-8') as configfile:
			parser.write(configfile)
			
		self.assertTrue(configfile)
		
		parser.read(config_path)

		if 'dummy' in parser.sections():
			location_config = parser['dummy']
			name, url = location_config['name'], location_config['url']

		self.assertEqual(location_config['name'], self.name)
		self.assertEqual(location_config['url'], self.url)

		os.remove(config_path)

	def test_clear_not_valid_cache(self):
		""" Test 'clear_not_valid_cache' method.
		"""

		cache = 'cache'
		file1 = 'cache_file'
		cache_path = Path.home() / cache

		if not cache_path.exists():
			cache_path.mkdir(parents=True)
		cache_dir= cache_path / file1

		timer = time.time() - self.cache_path.stat().st_mtime
		cache_time = 5
		is_valid = timer < cache_time

		if cache_path.exists():
			for file in os.listdir(cache_path):
				if not is_valid(cache_path/file):
					os.remove(cache_path/file)

		self.assertTrue(cache_path)
		self.assertTrue(cache_dir)

		rmtree(cache_path)

		if not cache_path.exists():
			n = 1

		self.assertEqual(n, 1)
		

if __name__ == '__main__':
	unittest.main()
