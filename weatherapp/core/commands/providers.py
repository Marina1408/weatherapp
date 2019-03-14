from weatherapp.core.abstract import Command


class Providers(Command):

	""" Print all available providers.
	"""

	name = 'providers'

	def run(self, argv):
		""" Run command.
		"""
		self.app.stdout.write('All available providers:' + '\n')

		for provider in self.app.providermanager._commands:
			self.app.stdout.write(f'{provider} \n')
