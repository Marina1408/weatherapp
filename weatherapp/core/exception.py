""" App exceptions
"""

class ProgramError(Exception):

	name = 'ProgramError'

	def __init__(self, data, name1):
		self.data = data
		self.name1 = name1

	def action(self):
		print(f'{self.name}, {self.name1}: {self.data}')


class WeatherProviderError(ProgramError):
	
	name = 'WeatherProviderError'


class RequestError(WeatherProviderError):

	name = 'RequestError'

	def action(self):
		print(f'{self.name}: {self.data}. Location = {self.name1} ???')


class ConfigParserError(WeatherProviderError):
	
	name = 'ConfigParserError'

	def action(self):
		print(f'{self.name}: {self.data}{self.name1}')
				

class AppRunError(ProgramError):
	
	name = 'AppRunError'

class ConfigurateCommandError(ProgramError):

	name = 'ConfigurateCommandError'

	


