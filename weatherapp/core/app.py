#!/usr/bin/env python

""" Main application module.
"""

import sys
import html
import logging
from argparse import ArgumentParser

from weatherapp.core.formatters import TableFormatter, ListFormatter
from weatherapp.core.providermanager import ProviderManager
from weatherapp.core.commandmanager import CommandManager
from weatherapp.core.commands import Configurate
from weatherapp.core import config
from weatherapp.core import decorators

@decorators.singleton
class App:

	""" Wether aggregator application.
	"""

	logger = logging.getLogger(__name__)
	LOG_LEVEL_MAP = {0: logging.WARNING,
	                 1: logging.INFO,
	                 2: logging.DEBUG}


	def __init__(self, stdin=None, stdout=None, stderr=None):
		self.stdin = stdin or sys.stdin
		self.stdout = stdout or sys.stdout
		self.stderr = stderr or sys.stderr
		self.arg_parser = self._arg_parse() 
		self.providermanager = ProviderManager()
		self.commandmanager = CommandManager()
		self.formatters = self._load_formatters()

	def _arg_parse(self):
		""" Initialize argument parser.
		"""

		arg_parser = ArgumentParser(add_help=False)
		arg_parser.add_argument('command', help='Service name', nargs='?')
		arg_parser.add_argument('--tomorrow', help='Weather for tomorrow day', 
                                action='store_true')
		arg_parser.add_argument('--write_file', 
                               help='Write the weather info to the text file', 
                                action='store_true')
		arg_parser.add_argument('--refresh', help='Bypass caches', 
                                action='store_true')
		arg_parser.add_argument('--reset_defaults', 
                                help='Clear configurate locations', 
                                action='store_true')
		arg_parser.add_argument('--debug', 
                             help='Show tracebacks on errors', 
                             action='store_true', default=False)
		arg_parser.add_argument('-v', '--verbose', action='count', 
			                    dest='verbose_level',
			                    default=config.DEFAULT_VERBOSE_LEVEL,
			                    help='Increase verbosity of output')
		arg_parser.add_argument('-f', '--formatter', action='store',
			                    default='list',
			                    help='Output format, defaults to table')

		return arg_parser

	@staticmethod
	def _load_formatters():
		return {'table': TableFormatter,
		         'list': ListFormatter}

	def configure_logging(self):
		""" Create logging handlers for any log output.
		"""

		root_logger = logging.getLogger('')
		root_logger.setLevel(logging.DEBUG)

		console = logging.StreamHandler()
		console_level = self.LOG_LEVEL_MAP.get(self.options.verbose_level,
			                                   logging.WARNING)
		console.setLevel(console_level)
		formatter = logging.Formatter(config.DEFAULT_MESSAGE_FORMAT)
		console.setFormatter(formatter)

		fl = logging.FileHandler('app.log')
		fl.setLevel(logging.ERROR)
		fl.setFormatter(formatter)

		root_logger.addHandler(console)
		root_logger.addHandler(fl)

	def produce_output(self, title, location, data):
	    """ Displays the final result of the program
	    """

	    formatter = self.formatters.get(self.options.formatter, 'list')()
	    columns = [title, location]

	    if self.options.tomorrow:
	    	self.stdout.write('Tomorrow: \n')
	    else:
	    	self.stdout.write('Today: \n')

	    self.stdout.write(formatter.emit(columns, data))
	    self.stdout.write('\n')

	    if self.options.write_file:
	    	self.write_file(title, location, data)

	def write_file(self, title, location, info):
		""" Write the weather data to text file.
		"""

		with open(config.WRITE_FILE, 'w') as f:
			if not self.options.tomorrow:
				f.write(title + '\n' + location + '\n' + str(info))
			else:
				f.write(title + '\n' + location + '  tomorrow' + 
					    '\n' + str(info))

	def run_command(self, name, argv):
		""" Run command.
		"""

		command = self.commandmanager.get(name)
		command = command(self)
		try:
			command.run(argv)
		except Exception:
			msg = ('Error during command: %s run.\n'
	    		   'The program can not continue to work!')
			if self.options.debug:
				self.logger.exception(msg, name)
			else:
				self.logger.error(msg, name)

	def run_provider(self, name, argv):
		""" Run specified provider.
		"""

		provider = self.providermanager.get(name)
		if provider:
			provider = provider(self)
			try:
				self.produce_output(provider.title, 
	    		                    provider.location, 
	    		                    provider.run(argv))
			except Exception:
				msg = ('Error during command: %s run.\n'
	    		       'The program can not continue to work!')
				if self.options.debug:
					self.logger.exception(msg, name)
				else:
					self.logger.error(msg, name)

	def run_providers(self, argv):
		""" Execute all available providers.
		"""

		for provider in self.providermanager._commands.values():
			provider = provider(self)
			try:
				self.produce_output(provider.title, 
					                provider.location, 
					                provider.run(argv))
			except Exception:
				msg = ('Error during command.\n'
					   'The program can not continue to work!')
				if self.options.debug:
					self.logger.exception(msg)
				else:
					self.logger.error(msg)

	def run(self, argv):
	    """ Run aplication.

	    :param argv: list of passed arguments
	    """

	    self.options, remaining_args = self.arg_parser.parse_known_args(argv)
	    self.configure_logging()
	    self.logger.debug('Got the following args %s', argv)

	    command_name = self.options.command
	    if not command_name:
	    	# run all command providers by default
	    	return self.run_providers(remaining_args)

	    if command_name in self.commandmanager:
	    	return self.run_command(command_name, remaining_args)

	    if command_name in self.providermanager:
	    	return self.run_provider(command_name, remaining_args)
		    	

def main(argv=sys.argv[1:]):
	""" Main entry point.
	"""
	
	return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])





