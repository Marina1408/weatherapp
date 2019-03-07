from weatherapp.core.providers import (AccuWeatherProvider, 
	                                   Rp5WeatherProvider, 
                                       SinoptikWeatherProvider)
from weatherapp.core import commandmanager

class ProviderManager(commandmanager.CommandManager):
	""" Discovers registered providers and loads them.
	"""

	def _load_commands(self):
		""" Loads all existing providers.
		"""

		for provider in [AccuWeatherProvider, 
		                 Rp5WeatherProvider,
		                 SinoptikWeatherProvider]:
		    self.add(provider.name, provider)

	
