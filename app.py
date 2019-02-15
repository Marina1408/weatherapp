#!/usr/bin/env python

""" Main application module.
"""

import sys
import html
from argparse import ArgumentParser

from providermanager import ProviderManager
import config

class App:

	""" Wether aggregator application.
	"""

	def __init__(self):
		self.arg_parser = self._arg_parse() 
		self.providermanager = ProviderManager()


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
		arg_parser.add_argument('clear-cache', 
                                help='Clear all cache with cache directory', 
                                nargs='?')
		arg_parser.add_argument('--reset_defaults', 
                                help='Clear configurate locations', 
                                action = 'store_true')

		return arg_parser

	def produse_output(self, title, location, info):
	    """ Displays the final result of the program
	    """

	    print(f'{title}:')
	    print("*"*10, end='\n\n')

	    print(f'{location}')
	    if self.options.tomorrow:
	    	print('Tomorrow:')
	    print('-'*20)
	    for key, value in info.items():
	    	print(f' {key} : {html.unescape(value)}')
	    	print("="*40, end='\n\n')

	def write_file(self, title, location, info):
		""" Write the weather data to text file.
		"""

		with open(config.WRITE_FILE, 'w') as f:
			f.write(str(self.produse_output(title, location, info)))

	def run(self, argv):
	    """ Run aplication.

	    :param argv: list of passed arguments
	    """

	    self.options, remaining_args = self.arg_parser.parse_known_args(argv)
	    command_name = self.options.command

	    if not command_name:
	    	for name, provider in self.providermanager._providers.items():
	    		provider_obj = provider(self)
	    		self.produse_output(provider_obj.title, 
	    			                provider_obj.location, 
	    			                provider_obj.run())
	    elif command_name in self.providermanager:
	    	provider = self.providermanager[command_name]
	    	provider_obj = provider(self)
	    	self.produse_output(provider_obj.title, 
	    		                provider_obj.location, 
	    		                provider_obj.run())

def main(argv=sys.argv[1:]):
	""" Main entry point.
	"""
	
	return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])





