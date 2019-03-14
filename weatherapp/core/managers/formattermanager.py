from weatherapp.core.abstract import Manager

from weatherapp.core.managers import commandmanager
from weatherapp.core.formatters import (TableFormatter, 
	                                    ListFormatter, 
	                                    CsvFormatter)


class FormatterManager(commandmanager.CommandManager):
	""" Manager for app formatters.
	"""


	def _load_commands(self):
		""" Loads all availble formatters.
		"""

		for command in [TableFormatter, ListFormatter, CsvFormatter]:
		    self.add(command.name, command)

	