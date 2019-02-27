#!/usr/bin/env python

""" Main application module.
"""

import sys
import html
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
                                action = 'store_true')
		arg_parser.add_argument('--write_file', 
                               help='Write the weather info to the text file', 
                                action = 'store_true')
		arg_parser.add_argument('--refresh', help='Bypass caches', 
                                action = 'store_true')
		arg_parser.add_argument('--reset_defaults', 
                                help='Clear configurate locations', 
                                action = 'store_true')

		return arg_parser

	def produce_output(self, title, location, info):
	    """ Displays the final result of the program
	    """

	    print(f'{title}:')
	    print("*"*12, end='\n\n')

	    print(f'{location}:')
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

	@decorators.timer
	def run(self, argv):
	    """ Run aplication.

	    :param argv: list of passed arguments
	    """

	    self.options, remaining_args = self.arg_parser.parse_known_args(argv)
	    command_name = self.options.command

	    if not command_name:
	    	# run all command providers by default.
	    	for name, provider in self.providermanager._commands.items():
	    		provider_obj = provider(self)
	    		self.produce_output(provider_obj.title, 
	    			                provider_obj.location, 
	    			                provider_obj.run(remaining_args))
	    elif command_name in self.providermanager:
	    	provider = self.providermanager[command_name]
	    	provider_obj = provider(self)
	    	self.produce_output(provider_obj.title, 
	    		                provider_obj.location, 
	    		                provider_obj.run(remaining_args))
	    elif command_name in self.commandmanager:
	    	command = self.commandmanager.get(command_name)
	    	command_obj = command(self)
	    	command_obj.run(remaining_args)
	    

def main(argv=sys.argv[1:]):
	""" Main entry point.
	"""
	
	return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])





