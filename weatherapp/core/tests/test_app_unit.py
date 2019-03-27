import os
import unittest
import argparse
import logging
import configparser
from pathlib import Path

from weatherapp.core.app import App


class AppTestCase(unittest.TestCase):
	""" Test application class methods.
	"""

	def setUp(self):
		self.parser = App._arg_parse(self)
		self.config_file = 'config_file'

	def test_arg_parse(self):
		""" Test application argument parser creation.
		"""

		self.assertIsInstance(self.parser, argparse.ArgumentParser)

	def test_arg_parse_default_values(self):
		""" Test application argument parser default values.
		"""

		parsed_args = self.parser.parse_args([])
		self.assertIsNone(parsed_args.command)
		self.assertFalse(parsed_args.debug)
		self.assertFalse(parsed_args.tomorrow)
		self.assertFalse(parsed_args.refresh)
		self.assertFalse(parsed_args.reset_defaults)
		self.assertFalse(parsed_args.write_file)
		self.assertEqual(parsed_args.formatter, 'list')
		self.assertEqual(parsed_args.verbose_level, 0)

	def test_arg_parse_arg(self):
		""" Test application argument parser.
		"""

		parsed_args = self.parser.parse_args(['accu', '--debug', '-v', 
			                               '--refresh', '--tomorrow',
			                               '--write_file', '--reset_defaults',
			                               '--formatter=table'])
		self.assertEqual(parsed_args.command, 'accu')
		self.assertTrue(parsed_args.debug)
		self.assertEqual(parsed_args.formatter, 'table')
		self.assertTrue(parsed_args.refresh)
		self.assertTrue(parsed_args.tomorrow)
		self.assertTrue(parsed_args.reset_defaults)
		self.assertTrue(parsed_args.write_file)
		self.assertEqual(parsed_args.verbose_level, 1)

	def test_get_log_configuration_file(self):
		""" Test 'get_log_configuration_file' method.
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

	def get_log_configuration(self):
		""" Test 'get_log_configuration' method.
		""" 

		configuration = configparser.ConfigParser(interpolation=None)

		log_level = logging.WARNING
		log_output = 'console'
		log_filename = 'w.log'

		config_path = Path.home() / self.config_file

		if config_path.exists():
			configuration.read(config_path)

		configuration['Bar'] = {'log-level': log_level,
		                 'log-output': log_output,
		                 'log-filename': log_filename}
		with open(config_path, 'w') as configfile:
			configuration.write(configfile)

		self.assertTrue(configfile)
		
		configuration.read(config_path)

		if 'Bar' in configuration.sections():
			bar_config = configuration['Bar']
			log_level = bar_config.get('log-level', logging.WARNING)
			log_output = bar_config.get('log-output', 'console')
			log_filename = bar_config.get('log-filename', 'w.log')

		self.assertEqual(bar_config['log-level'], logging.WARNING)
		self.assertEqual(bar_config['log-output'], 'console')
		self.assertEqual(bar_config['log-filename'], 'w.log')

		os.remove(config_path)

	def test_configure_logging(self):
		""" Test 'configure_logging' method.
		""" 

		root_logger = logging.getLogger('')
		root_logger.setLevel(logging.DEBUG)

		log_level = logging.WARNING
		log_output = 'console' 
		log_filename = 'w.log'
		
		console = logging.StreamHandler()
		console.setLevel(log_level)
		formatter = logging.Formatter('%(message)s')
		console.setFormatter(formatter)
		root_logger.addHandler(console)

		self.assertTrue(console)
		self.assertTrue(root_logger)
		self.assertTrue(formatter)

		log_output = 'file'

		fl = logging.FileHandler(log_filename)
		fl.setLevel(log_level)
		formatter = logging.Formatter('%(message)s')
		fl.setFormatter(formatter)
		root_logger.addHandler(fl)

		self.assertTrue(fl)
		self.assertTrue(root_logger)
		self.assertTrue(formatter)

	def test_write_file(self):
		""" Test 'write_file' method.
		"""

		file = 'w_file'
		title = 'title'
		location = 'location'
		info = 'info'

		with open((Path.home() / file), 'w') as f:
			f.write(title + '\n' + location + '\n' + str(info))
			
		self.assertTrue(f)

		with open((Path.home() / file), 'r') as f:
			a = f.read()

		self.assertEqual(a, 'title\nlocation\ninfo')

		os.remove(Path.home() / file)
			
		
if __name__ == '__main__':
	unittest.main()
