import io
import os
import argparse
import unittest
from pathlib import Path
from shutil import rmtree

from weatherapp.core.app import App
from weatherapp.core.abstract import Command
from weatherapp.core.commands import Configurate


class CommandsTestCase(unittest.TestCase):

	""" Test case for commands tests.
	"""

	def test_providers(self):
		""" Test providers command.
		"""

		stdout = io.StringIO()
		App(stdout=stdout).run(['providers'])
		stdout.seek(0)
	
		self.assertEqual(stdout.read(), ('All available providers:\nsinoptik' 
			                             ' \naccu \nrp5 \n'))

	def test_clear_cache_dir(self):
	    """ Test clear_cache_dir command.
	    """

	    cache = '.wappcache'
	    cache_dir = Path.home() / cache
	    if not cache_dir.exists():
	    	os.makedirs(cache_dir)

	    stdout = io.StringIO()
	    App(stdout=stdout).run(['clear_cache'])
	    stdout.seek(0)

	    self.assertEqual(stdout.read(), 'Clear all cache files. \n')

	def test_configurate(self):
	    """ Test configurate command.
	    """

	    self.parser = App._arg_parse(self)
	    self.assertIsInstance(self.parser, argparse.ArgumentParser)
	    parsed_args = self.parser.parse_args(['configurate'])
	    self.assertEqual(parsed_args.command, 'configurate')
	    self.assertFalse(parsed_args.reset_defaults)

	    parsed_args = self.parser.parse_args(['configurate', 
	    	                                  '--reset_defaults'])
	    self.assertEqual(parsed_args.command, 'configurate')
	    self.assertTrue(parsed_args.reset_defaults)


if __name__ == '__main__':
	unittest.main()



	    

			                            
	    
			                             


