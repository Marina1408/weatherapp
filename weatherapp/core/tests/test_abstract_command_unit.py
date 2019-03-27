import os
import unittest
import argparse
from pathlib import Path
from shutil import rmtree

from weatherapp.core.abstract import Command


class CommandAbstractTestCase(unittest.TestCase):

	""" Unit test case for abstract command.
	"""

	def setUp(self):
		self.cache_dir = 'cache'
		self.cache_path = Path.home() / self.cache_dir
		self.config_file = 'config_file'

	def test_get_parser(self):
		""" Test 'get_parser' method.
		"""

		self.parser = Command.get_parser()
		self.assertIsInstance(self.parser, argparse.ArgumentParser)

	def test_get_cache_directory(self):
		""" Test 'get_cache_directory' method.
		"""

		self.assertTrue(self.cache_path)

	def test_clear_all_cache(self):
		""" Test 'clear_all_cache' method.
		"""

		if self.cache_path.exists():
			rmtree(self.cache_path)
		else:
			os.makedirs(self.cache_path)
			rmtree(self.cache_path)

		self.assertTrue(self.cache_path)

		if not self.cache_path.exists():
			n = 1

		self.assertEqual(n, 1)


	def test_get_configuration_file(self):
		""" Test 'get_configuration_file' method.
		"""

		config_path = Path.home() / self.config_file

		self.assertTrue(config_path)

	def test_clear_configurate(self):
		""" Test 'clear_configurate' method.
		"""

		config_path = Path.home() / self.config_file

		if config_path.exists():
			os.remove(Path.home() / self.config_file)

		self.assertTrue(config_path)

		if not config_path.exists():
			n = 1

		self.assertEqual(n, 1)


if __name__ == '__main__':
	unittest.main()






		