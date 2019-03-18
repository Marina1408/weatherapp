""" App exceptions
"""

from weatherapp.core.abstract import Command


class ProgramError(Command, Exception):

	name = 'ProgramError'


	def run(self,data, module_name):
		self.app.stdout.write(f'{self.name}, {module_name}: {data}\n')


class WeatherProviderError(ProgramError):
	
	name = 'WeatherProviderError'


class RequestError(WeatherProviderError):

	name = 'RequestError'

	def run(self, data, location):
		self.app.stdout.write(f'{self.name}: {data}. Location = {location} ???\n')


class ConfigParserError(WeatherProviderError):
	
	name = 'ConfigParserError'

	def run(self, data, module_name):
		self.app.stdout.write(f'{self.name}: {data} {module_name}\n')
				

class AppRunError(ProgramError):
	
	name = 'AppRunError'

class ConfigurateCommandError(ProgramError):

	name = 'ConfigurateCommandError'

	


