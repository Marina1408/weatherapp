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

	def test_configurate(self):
	    """ Test configurate command.
	    """

	    self.parser = argparse.ArgumentParser()
	    self.parser.add_argument('provider', help='Provider name', nargs='?')
	    self.assertIsInstance(self.parser, argparse.ArgumentParser)
	    parsed_args = self.parser.parse_args(['accu'])
	    self.assertEqual(parsed_args.provider, 'accu')

	    self.parser = argparse.ArgumentParser()
	    self.parser.add_argument('provider', help='Provider name', nargs='?')
	    parsed_args = self.parser.parse_args([])
	    self.assertIsNone(parsed_args.provider)


if __name__ == '__main__':
	unittest.main()