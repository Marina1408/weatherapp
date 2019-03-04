#!/usr/bin/env python

""" Main application module.
"""

import sys
import html
import logging
from argparse import ArgumentParser

from providermanager import ProviderManager
from commandmanager import CommandManager
from commands import Configurate

import config
import decorators

@decorators.singleton
class App:

	""" Wether aggregator application.
	"""

	logger = logging.getLogger(__name__)
	LOG_LEVEL_MAP = {0: logging.WARNING,
	                 1: logging.INFO,
	                 2: logging.DEBUG}


	def __init__(self):
		self.arg_parser = self._arg_parse() 
		self.providermanager = ProviderManager()
		self.commandmanager = CommandManager()

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

		return arg_parser

	def configure_logging(self):
		""" Create logging handlers for any log output.
		"""

		root_logger = logging.getLogger('')
		root_logger.setLevel(logging.DEBUG)

		console = logging.StreamHandler()
		console_level = self.LOG_LEVEL_MAP.get(self.options.verbose_level,
			                                   logging.WARNING)
		console.setLevel(console_level)
		fl = logging.FileHandler('app.log')
		fl.setLevel(logging.WARNING)
		formatter = logging.Formatter(config.DEFAULT_MESSAGE_FORMAT)
		console.setFormatter(formatter)
		fl.setFormatter(formatter)
		root_logger.addHandler(console)
		root_logger.addHandler(fl)

	def produce_output(self, title, location, info):
	    """ Displays the final result of the program
	    """

	    print(f'{title}:')
	    print("*"*12, end='\n\n')

	    print(f'{location.capitalize()}:')
	    if self.options.tomorrow:
	    	print('Tomorrow:')
	    print('-'*12)
	    for key, value in info.items():
	    	print(f' {key} : {html.unescape(value)}')
	    	print("="*40, end='\n\n')

	    if self.options.write_file:
	    	self.write_file(title, location, info)

	def write_file(self, title, location, info):
		""" Write the weather data to text file.
		"""

		with open(config.WRITE_FILE, 'w') as f:
			if not self.options.tomorrow:
				f.write(title + '\n' + location + '\n' + str(info))
			else:
				f.write(title + '\n' + location + '  tomorrow' + 
					    '\n' + str(info))

	def run(self, argv):
	    """ Run aplication.

	    :param argv: list of passed arguments
	    """

	    self.options, remaining_args = self.arg_parser.parse_known_args(argv)
	    self.configure_logging()
	    self.logger.debug('Got the following args %s', argv)
	    command_name = self.options.command

	    if not command_name:
	    	# run all command providers by default.
	    	for name, provider in self.providermanager._commands.items():
	    		provider_obj = provider(self)
	    		try:
	    		    self.produce_output(provider_obj.title, 
	    			                    provider_obj.location, 
	    			                    provider_obj.run(remaining_args))
	    		except Exception:
	    		    msg = ('Error during command: %s run.\n'
	    		           'The program can not continue to work!')
	    		    if self.options.debug:
	    			    self.logger.exception(msg, command_name)
	    		    else:
	    			    self.logger.error(msg, command_name)	
	    elif command_name in self.providermanager:
	    	provider = self.providermanager[command_name]
	    	provider_obj = provider(self)
	    	try:
	    		self.produce_output(provider_obj.title, 
	    		                    provider_obj.location, 
	    		                    provider_obj.run(remaining_args))
	    	except Exception:
	    		msg = ('Error during command: %s run.\n'
	    		       'The program can not continue to work!')
	    		if self.options.debug:
	    			self.logger.exception(msg, command_name)
	    		else:
	    			self.logger.error(msg, command_name)	
	    elif command_name in self.commandmanager:
	    	command = self.commandmanager.get(command_name)
	    	command_obj = command(self)
	    	try:
	    		command_obj.run(remaining_args)
	    	except Exception:
	    		msg = ('Error during command: %s run.\n'
	    		       'The program can not continue to work!')
	    		if self.options.debug:
	    			self.logger.exception(msg, command_name)
	    		else:
	    			self.logger.error(msg, command_name)
	    	

def main(argv=sys.argv[1:]):
	""" Main entry point.
	"""
	
	return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])





