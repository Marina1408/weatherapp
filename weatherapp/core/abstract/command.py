import os
import abc
import argparse
from pathlib import Path
from shutil import rmtree

from weatherapp.core import config

class Command(abc.ABC):

	""" Base class for commands.

	:param app: Main application instance
	:type app: app.App
	"""

	def __init__(self, app):
		self.app = app

	@staticmethod
	def get_parser():
		""" Initialize argument parser for command.
		"""

		parser = argparse.ArgumentParser()
		return parser

	@abc.abstractmethod
	def run(self, argv):
	    """ Invoked by application when the command is run.

	    Should be overriden in subclass.
	    """

	@staticmethod
	def get_cache_directory():
	    """ Return home directory to cach files.
	    """

	    return Path.home() / config.CACHE_DIR

	def clear_all_cache(self):
	    """ Clear all cache files and the cache directory.
	    """

	    cache_dir = self.get_cache_directory()
	    rmtree(cache_dir)

	@staticmethod
	def get_configuration_file():
	    """ Path to configuration file.

	    Returns path to configuration file in your home directory.
	    """

	    return Path.home() / config.CONFIG_FILE 

	def clear_configurate(self):
	    """ Clear configurate file for weather site.
	    """

	    os.remove(self.get_configuration_file())

