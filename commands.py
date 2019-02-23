""" App commands.
"""

from abstract import Command, WeatherProvider


class Configurate(Command):

	""" Help to configure weather providers.
	"""

	name = 'configurate'

	def get_parser(self):
		parser = super().get_parser()
		parser.add_argument('provider', help='Provider name')
		print(3)
		return parser

	def run(self, argv):
		print(0)
		parsed_args = self.get_parser().parse_args(argv)
		print(1)
		if parsed_args.provider:
			print(4)
			provider_name = parsed_args.provider
			if provider_name in self.app.providermanager:
				provider_factory = self.app.providermanager.get(provider_name)
				provider_factory(self.app).configurate()
		else:
			print('No!')


class Providers(Command):

	""" Print all available providers.
	"""

	name = 'providers'

	def run(self, argv):
		""" Run command.
		"""
		print('All available providers:')

		for provider in self.app.providermanager._commands:
			print(provider)


class ClearCacheDir(Command):

	""" Clear all cache files and the cach directory.
	"""

	name = 'clear_cache'

	def run(self, argv):
		""" Run command.
		"""

		self.clear_all_cache()

			
