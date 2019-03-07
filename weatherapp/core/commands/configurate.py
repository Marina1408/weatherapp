import logging

from weatherapp.core import config
from weatherapp.core.abstract import Command


class Configurate(Command):

	""" Help to configure weather providers.
	"""

	name = 'configurate'
	logger = logging.getLogger(__name__)

	def get_parser(self):
		parser = super().get_parser()
		parser.add_argument('provider', help='Provider name', nargs='?')
		return parser

	def run(self, argv):
		""" Run command.
		"""

		params = self.get_parser().parse_args(argv)

		if params.provider:
			provider_name = params.provider
			if provider_name in self.app.providermanager:
				provider_factory = \
					    self.app.providermanager.get(provider_name)
				provider_factory(self.app).configurate()
		else:
			if self.app.options.reset_defaults:
				self.clear_configurate()
				print('The configuration file is deleted!')
			else:
				self.logging_configuration()

	def logging_configuration(self):
		"""
		"""

		menu = {1: 'login level',
		        2: 'logging into a file or console',
		        3: 'name of the log file'}

		for key, value in menu.items():
			print(key, value)
		selected_index = int(input('Please select number: '))
		if selected_index in menu:
			if selected_index == 1:
				self.login_level()
			elif selected_index == 2:
				pass
			elif selected_index == 3:
				pass	
		else:
			print('You have entered an invalid number!')

	def login_level(self):
		"""
		"""

		LOG_LEVEL_MAP = {0: logging.WARNING, 
		                 1: logging.INFO, 
		                 2: logging.DEBUG}

		for key, value in LOG_LEVEL_MAP.items():
			print(key, value)
		choice_level = int(input('Please select index: '))
		if choice_level in LOG_LEVEL_MAP:
			pass
		else:
			print('You have entered an invalid index!')

